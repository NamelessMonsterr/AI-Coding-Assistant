import * as vscode from 'vscode';
import { AIService } from '../services/aiService';
import * as path from 'path';
import * as fs from 'fs';

interface Message {
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp?: Date;
    actions?: Action[];
}

interface Action {
    type: 'create_file' | 'edit_file' | 'execute' | 'terminal_command';
    file?: string;
    content?: string;
    command?: string;
    status?: 'pending' | 'success' | 'error';
    result?: string;
}

export class ChatViewProvider implements vscode.WebviewViewProvider {
    private _view?: vscode.WebviewView;
    private chatHistory: Message[] = [];
    private contextFiles: Set<string> = new Set();
    private workspaceAnalysis: any = null;
    private terminal?: vscode.Terminal;
    private autoExecuteEnabled: boolean = true;
    private fileWatcher?: vscode.FileSystemWatcher;

    constructor(
        private readonly _extensionUri: vscode.Uri,
        private aiService: AIService
    ) {
        this.setupFileWatcher();
        this.setupTerminal();
    }

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken,
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

        // Handle messages from webview
        webviewView.webview.onDidReceiveMessage(async (data) => {
            switch (data.type) {
                case 'sendMessage':
                    await this.handleUserMessage(data.message);
                    break;
                case 'executeAction':
                    await this.executeAction(data.action);
                    break;
                case 'toggleAutoExecute':
                    this.autoExecuteEnabled = data.enabled;
                    break;
                case 'openTerminal':
                    this.showTerminal();
                    break;
                case 'clearChat':
                    this.clearChat();
                    break;
                case 'insertCode':
                    this.insertCodeIntoEditor(data.code);
                    break;
                case 'selectModel':
                    await this.selectModel();
                    break;
                case 'addCurrentFile':
                    await this.addCurrentFileToContext();
                    break;
                case 'analyzeWorkspace':
                    await this.analyzeWorkspace();
                    break;
                case 'addFileToContext':
                    await this.addFileToContext();
                    break;
                case 'removeFile':
                    this.removeFileFromContext(data.file);
                    break;
                case 'clearContext':
                    this.clearFileContext();
                    break;
            }
        });

        // Send initial context
        this.updateContextUI();
    }

    private setupFileWatcher() {
        // Watch for active editor changes
        vscode.window.onDidChangeActiveTextEditor((editor) => {
            if (editor) {
                this.updateContextUI();
            }
        });

        // Watch for file changes in workspace
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (workspaceFolder) {
            this.fileWatcher = vscode.workspace.createFileSystemWatcher(
                new vscode.RelativePattern(workspaceFolder, '**/*')
            );

            this.fileWatcher.onDidChange((uri) => {
                this.notifyFileChange('modified', uri);
            });

            this.fileWatcher.onDidCreate((uri) => {
                this.notifyFileChange('created', uri);
            });

            this.fileWatcher.onDidDelete((uri) => {
                this.notifyFileChange('deleted', uri);
            });
        }
    }

    private setupTerminal() {
        // Create integrated terminal
        this.terminal = vscode.window.createTerminal({
            name: 'AI Assistant',
            hideFromUser: false
        });

        // Listen to terminal output (VS Code doesn't provide direct API, so we track commands)
        vscode.window.onDidChangeActiveTerminal((terminal) => {
            if (terminal?.name === 'AI Assistant') {
                this.terminal = terminal;
            }
        });
    }

    private notifyFileChange(type: string, uri: vscode.Uri) {
        const fileName = path.basename(uri.fsPath);
        this._view?.webview.postMessage({
            type: 'fileChanged',
            changeType: type,
            file: fileName,
            path: uri.fsPath
        });
    }

    private async handleUserMessage(message: string) {
        // Add user message
        this.chatHistory.push({
            role: 'user',
            content: message,
            timestamp: new Date()
        });
        this.updateChatUI();

        // Show loading
        this._view?.webview.postMessage({ type: 'loading', value: true });

        try {
            // Build context from files
            const contextInfo = await this.buildFileContext();

            // Detect intent and check if it requires autonomous actions
            const intent = this.detectIntent(message);
            let response = '';
            let actions: Action[] = [];

            if (this.shouldUseAutonomousMode(message)) {
                // Use autonomous mode with action planning
                const aiResponse = await this.getAIResponseWithActions(message, contextInfo, intent);
                response = aiResponse.content;
                actions = aiResponse.actions;

                // Auto-execute actions if enabled
                if (this.autoExecuteEnabled && actions.length > 0) {
                    await this.executeActionsSequentially(actions);
                }
            } else {
                // Use regular chat mode
                switch (intent) {
                    case 'generate':
                        response = await this.handleGenerate(message, contextInfo);
                        break;
                    case 'explain':
                        response = await this.handleExplain(message, contextInfo);
                        break;
                    case 'review':
                        response = await this.handleReview(message, contextInfo);
                        break;
                    case 'refactor':
                        response = await this.handleRefactor(message, contextInfo);
                        break;
                    case 'analyze':
                        response = await this.handleAnalyze(message, contextInfo);
                        break;
                    default:
                        response = await this.handleChat(message, contextInfo);
                }
            }

            // Add assistant response
            this.chatHistory.push({
                role: 'assistant',
                content: response,
                timestamp: new Date(),
                actions: actions
            });
            this.updateChatUI();

        } catch (error: any) {
            this.chatHistory.push({
                role: 'assistant',
                content: `❌ Error: ${error.message || 'Something went wrong'}`,
                timestamp: new Date()
            });
            this.updateChatUI();
        } finally {
            this._view?.webview.postMessage({ type: 'loading', value: false });
        }
    }

    private async buildFileContext(): Promise<string> {
        let context = '';

        // Add current file context
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const fileName = path.basename(editor.document.fileName);
            const language = editor.document.languageId;
            const selection = editor.document.getText(editor.selection);

            context += `\n**Current File:** ${fileName} (${language})\n`;

            if (selection) {
                context += `**Selected Code:**\n\`\`\`${language}\n${selection}\n\`\`\`\n`;
            }
        }

        // Add context files
        if (this.contextFiles.size > 0) {
            context += `\n**Context Files (${this.contextFiles.size}):**\n`;

            for (const filePath of this.contextFiles) {
                try {
                    const content = fs.readFileSync(filePath, 'utf8');
                    const fileName = path.basename(filePath);
                    const ext = path.extname(filePath);
                    const language = this.getLanguageFromExtension(ext);

                    // Limit file size
                    const truncatedContent = content.length > 2000
                        ? content.substring(0, 2000) + '\n... (truncated)'
                        : content;

                    context += `\n**${fileName}:**\n\`\`\`${language}\n${truncatedContent}\n\`\`\`\n`;
                } catch (error) {
                    console.error(`Error reading file ${filePath}:`, error);
                }
            }
        }

        // Add workspace analysis if available
        if (this.workspaceAnalysis) {
            context += `\n**Workspace Structure:**\n${JSON.stringify(this.workspaceAnalysis, null, 2)}\n`;
        }

        return context;
    }

    private async handleGenerate(message: string, contextInfo: string): Promise<string> {
        const language = this.detectLanguage(message);
        const fullPrompt = `${contextInfo}\n\n**User Request:** ${message}`;

        const result = await this.aiService.generateCode(fullPrompt, language);
        return result.success
            ? `\`\`\`${language}\n${result.data.code}\n\`\`\``
            : result.message || 'Error generating code';
    }

    private async handleExplain(message: string, contextInfo: string): Promise<string> {
        const editor = vscode.window.activeTextEditor;
        const code = editor?.document.getText(editor.selection) || '';
        const language = editor?.document.languageId || 'text';

        const fullPrompt = `${contextInfo}\n\nExplain this code:\n\`\`\`${language}\n${code}\n\`\`\`\n\nUser question: ${message}`;

        const result = await this.aiService.generateCode(fullPrompt, language);
        return result.success ? result.data.code : result.message || 'Error explaining code';
    }

    private async handleReview(message: string, contextInfo: string): Promise<string> {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            return '❌ No file is currently open';
        }

        const code = editor.document.getText();
        const language = editor.document.languageId;
        const fileName = path.basename(editor.document.fileName);

        const result = await this.aiService.reviewCode(code, language, fileName);
        return result.success ? result.data.review : result.message || 'Error reviewing code';
    }

    private async handleRefactor(message: string, contextInfo: string): Promise<string> {
        const editor = vscode.window.activeTextEditor;
        const code = editor?.document.getText(editor.selection) || '';
        const language = editor?.document.languageId || 'text';

        const fullPrompt = `${contextInfo}\n\nRefactor this code:\n\`\`\`${language}\n${code}\n\`\`\`\n\nRequirements: ${message}`;

        const result = await this.aiService.generateCode(fullPrompt, language);
        return result.success
            ? `\`\`\`${language}\n${result.data.code}\n\`\`\``
            : result.message || 'Error refactoring code';
    }

    private async handleAnalyze(message: string, contextInfo: string): Promise<string> {
        const analysis = await this.performMultiFileAnalysis();
        return `**Multi-File Analysis:**\n\n${analysis}`;
    }

    private async handleChat(message: string, contextInfo: string): Promise<string> {
        const fullPrompt = contextInfo
            ? `${contextInfo}\n\n**User:** ${message}`
            : message;

        const result = await this.aiService.generateCode(fullPrompt, 'text');
        return result.success ? result.data.code : result.message || 'Error processing request';
    }

    private async addCurrentFileToContext() {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const filePath = editor.document.fileName;
            this.contextFiles.add(filePath);
            this.updateContextUI();
            vscode.window.showInformationMessage(`Added ${path.basename(filePath)} to context`);
        }
    }

    private async addFileToContext() {
        const files = await vscode.window.showOpenDialog({
            canSelectMany: true,
            openLabel: 'Add to Context'
        });

        if (files) {
            files.forEach(file => this.contextFiles.add(file.fsPath));
            this.updateContextUI();
            vscode.window.showInformationMessage(`Added ${files.length} file(s) to context`);
        }
    }

    private removeFileFromContext(filePath: string) {
        this.contextFiles.delete(filePath);
        this.updateContextUI();
    }

    private clearFileContext() {
        this.contextFiles.clear();
        this.workspaceAnalysis = null;
        this.updateContextUI();
        vscode.window.showInformationMessage('Context cleared');
    }

    private async analyzeWorkspace() {
        vscode.window.showInformationMessage('Analyzing workspace...');

        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            vscode.window.showWarningMessage('No workspace folder open');
            return;
        }

        this._view?.webview.postMessage({ type: 'loading', value: true });

        try {
            const analysis = await this.performWorkspaceAnalysis(workspaceFolder.uri.fsPath);
            this.workspaceAnalysis = analysis;

            // Add analysis to chat
            this.chatHistory.push({
                role: 'system',
                content: `📊 **Workspace Analyzed:**\n\n${this.formatWorkspaceAnalysis(analysis)}`,
                timestamp: new Date()
            });

            this.updateChatUI();
            this.updateContextUI();
            vscode.window.showInformationMessage('Workspace analysis complete!');
        } catch (error: any) {
            vscode.window.showErrorMessage(`Analysis failed: ${error.message}`);
        } finally {
            this._view?.webview.postMessage({ type: 'loading', value: false });
        }
    }

    private async performWorkspaceAnalysis(rootPath: string): Promise<any> {
        const analysis = {
            totalFiles: 0,
            filesByLanguage: {} as Record<string, number>,
            structure: {} as any,
            imports: [] as string[],
            functions: [] as string[],
            classes: [] as string[]
        };

        const files = await vscode.workspace.findFiles('**/*.{js,ts,py,java,cpp,go,rs}', '**/node_modules/**');
        analysis.totalFiles = files.length;

        for (const file of files.slice(0, 100)) { // Limit to 100 files
            const ext = path.extname(file.fsPath);
            const language = this.getLanguageFromExtension(ext);

            analysis.filesByLanguage[language] = (analysis.filesByLanguage[language] || 0) + 1;

            // Basic code analysis
            try {
                const content = fs.readFileSync(file.fsPath, 'utf8');

                // Extract imports (simple regex)
                const importMatches = content.match(/import\s+.*?from\s+['"](.+?)['"]/g);
                if (importMatches) {
                    importMatches.forEach(imp => {
                        const match = imp.match(/from\s+['"](.+?)['"]/);
                        if (match) analysis.imports.push(match[1]);
                    });
                }

                // Extract functions
                const funcMatches = content.match(/(?:function|def|func)\s+(\w+)/g);
                if (funcMatches) {
                    funcMatches.forEach(f => {
                        const match = f.match(/(?:function|def|func)\s+(\w+)/);
                        if (match) analysis.functions.push(match[1]);
                    });
                }

                // Extract classes
                const classMatches = content.match(/class\s+(\w+)/g);
                if (classMatches) {
                    classMatches.forEach(c => {
                        const match = c.match(/class\s+(\w+)/);
                        if (match) analysis.classes.push(match[1]);
                    });
                }
            } catch (error) {
                console.error(`Error analyzing ${file.fsPath}:`, error);
            }
        }

        return analysis;
    }

    private async performMultiFileAnalysis(): Promise<string> {
        if (this.contextFiles.size === 0) {
            return '❌ No files in context. Add files using the "Add File" button.';
        }

        let analysis = `**Multi-File Analysis (${this.contextFiles.size} files):**\n\n`;

        const fileContents: { name: string; content: string; language: string }[] = [];

        for (const filePath of this.contextFiles) {
            try {
                const content = fs.readFileSync(filePath, 'utf8');
                const fileName = path.basename(filePath);
                const ext = path.extname(filePath);
                const language = this.getLanguageFromExtension(ext);

                fileContents.push({ name: fileName, content, language });
            } catch (error) {
                console.error(`Error reading ${filePath}:`, error);
            }
        }

        // Analyze relationships
        analysis += '**Dependencies:**\n';
        fileContents.forEach(file => {
            const imports = this.extractImports(file.content);
            if (imports.length > 0) {
                analysis += `- ${file.name}: imports ${imports.join(', ')}\n`;
            }
        });

        // Analyze complexity
        analysis += '\n**Complexity:**\n';
        fileContents.forEach(file => {
            const lines = file.content.split('\n').length;
            const functions = (file.content.match(/(?:function|def|func)\s+\w+/g) || []).length;
            analysis += `- ${file.name}: ${lines} lines, ${functions} functions\n`;
        });

        return analysis;
    }

    private extractImports(content: string): string[] {
        const imports: string[] = [];

        // JavaScript/TypeScript imports
        const jsImports = content.match(/import\s+.*?from\s+['"](.+?)['"]/g);
        if (jsImports) {
            jsImports.forEach(imp => {
                const match = imp.match(/from\s+['"](.+?)['"]/);
                if (match) imports.push(match[1]);
            });
        }

        // Python imports
        const pyImports = content.match(/(?:from\s+(\S+)\s+)?import\s+(.+)/g);
        if (pyImports) {
            pyImports.forEach(imp => {
                const match = imp.match(/(?:from\s+(\S+)\s+)?import\s+(.+)/);
                if (match) imports.push(match[1] || match[2]);
            });
        }

        return imports;
    }

    private formatWorkspaceAnalysis(analysis: any): string {
        let formatted = `**Total Files:** ${analysis.totalFiles}\n\n`;

        formatted += '**Files by Language:**\n';
        Object.entries(analysis.filesByLanguage).forEach(([lang, count]) => {
            formatted += `- ${lang}: ${count}\n`;
        });

        if (analysis.functions.length > 0) {
            formatted += `\n**Functions Found:** ${analysis.functions.length}\n`;
        }

        if (analysis.classes.length > 0) {
            formatted += `**Classes Found:** ${analysis.classes.length}\n`;
        }

        return formatted;
    }

    private detectIntent(message: string): string {
        const lowerMessage = message.toLowerCase();

        if (lowerMessage.includes('generate') || lowerMessage.includes('create') || lowerMessage.includes('write')) {
            return 'generate';
        } else if (lowerMessage.includes('explain') || lowerMessage.includes('what does') || lowerMessage.includes('understand')) {
            return 'explain';
        } else if (lowerMessage.includes('review') || lowerMessage.includes('check') || lowerMessage.includes('audit')) {
            return 'review';
        } else if (lowerMessage.includes('refactor') || lowerMessage.includes('improve') || lowerMessage.includes('optimize')) {
            return 'refactor';
        } else if (lowerMessage.includes('analyze') || lowerMessage.includes('workspace') || lowerMessage.includes('project')) {
            return 'analyze';
        }

        return 'chat';
    }

    private detectLanguage(message: string): string {
        const languages = ['python', 'javascript', 'typescript', 'java', 'cpp', 'go', 'rust', 'html', 'css'];
        for (const lang of languages) {
            if (message.toLowerCase().includes(lang)) {
                return lang;
            }
        }
        return vscode.window.activeTextEditor?.document.languageId || 'python';
    }

    private getLanguageFromExtension(ext: string): string {
        const languageMap: Record<string, string> = {
            '.js': 'javascript',
            '.ts': 'typescript',
            '.py': 'python',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.md': 'markdown'
        };
        return languageMap[ext] || 'text';
    }

    private updateChatUI() {
        this._view?.webview.postMessage({
            type: 'updateChat',
            messages: this.chatHistory
        });
    }

    private updateContextUI() {
        const contextFilesList = Array.from(this.contextFiles).map(f => ({
            path: f,
            name: path.basename(f)
        }));

        const currentFile = vscode.window.activeTextEditor
            ? {
                path: vscode.window.activeTextEditor.document.fileName,
                name: path.basename(vscode.window.activeTextEditor.document.fileName),
                language: vscode.window.activeTextEditor.document.languageId
            }
            : null;

        this._view?.webview.postMessage({
            type: 'updateContext',
            contextFiles: contextFilesList,
            currentFile: currentFile,
            hasWorkspaceAnalysis: !!this.workspaceAnalysis
        });
    }

    public clearChat() {
        this.chatHistory = [];
        this.updateChatUI();
    }

    private insertCodeIntoEditor(code: string) {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            editor.edit(editBuilder => {
                editBuilder.insert(editor.selection.active, code);
            });
        }
    }

    private async selectModel() {
        const models = await this.aiService.getAvailableModels();
        const selected = await vscode.window.showQuickPick(models, {
            placeHolder: 'Select AI Model'
        });
        if (selected) {
            const config = vscode.workspace.getConfiguration('unified-ai');
            await config.update('defaultModel', selected, vscode.ConfigurationTarget.Global);
            vscode.window.showInformationMessage(`Switched to ${selected} model`);
        }
    }

    private shouldUseAutonomousMode(message: string): boolean {
        const lowerMessage = message.toLowerCase();
        return lowerMessage.includes('create') || lowerMessage.includes('generate') || lowerMessage.includes('fix') || lowerMessage.includes('implement');
    }

    private async getAIResponseWithActions(message: string, contextInfo: string, intent: string): Promise<{ content: string; actions: Action[] }> {
        const prompt = `${contextInfo}\n\nUser request: ${message}\n\nPlease provide a response and suggest actions if applicable. Actions should be in JSON format.`;

        const result = await this.aiService.generateCode(prompt, 'text');
        if (result.success) {
            // Parse actions from response (assuming AI returns JSON with actions)
            let actions: Action[] = [];
            try {
                const parsed = JSON.parse(result.data.code);
                actions = parsed.actions || [];
            } catch (e) {
                // No actions
            }
            return { content: result.data.code, actions };
        }
        return { content: result.message || 'Error', actions: [] };
    }

    private async executeActionsSequentially(actions: Action[]): Promise<void> {
        for (const action of actions) {
            await this.executeAction(action);
        }
    }

    private async executeAction(action: Action): Promise<void> {
        try {
            switch (action.type) {
                case 'create_file':
                    if (action.file && action.content) {
                        await vscode.workspace.fs.writeFile(vscode.Uri.file(action.file), Buffer.from(action.content));
                        action.status = 'success';
                    }
                    break;
                case 'edit_file':
                    if (action.file && action.content) {
                        const uri = vscode.Uri.file(action.file);
                        const existing = await vscode.workspace.fs.readFile(uri);
                        const newContent = existing.toString().replace(action.content, ''); // Simple replace, adjust as needed
                        await vscode.workspace.fs.writeFile(uri, Buffer.from(newContent));
                        action.status = 'success';
                    }
                    break;
                case 'execute':
                    if (action.command) {
                        const terminal = vscode.window.createTerminal('AI Action');
                        terminal.sendText(action.command);
                        terminal.show();
                        action.status = 'success';
                    }
                    break;
                case 'terminal_command':
                    if (action.command) {
                        this.terminal?.sendText(action.command);
                        action.status = 'success';
                    }
                    break;
            }
        } catch (error) {
            action.status = 'error';
            action.result = error instanceof Error ? error.message : 'Unknown error';
        }
    }

    private showTerminal(): void {
        this.terminal?.show();
    }

    private _getHtmlForWebview(webview: vscode.Webview): string {
        const htmlPath = path.join(this._extensionUri.fsPath, 'src', 'views', 'chat.html');
        return fs.readFileSync(htmlPath, 'utf8');
    }
}
