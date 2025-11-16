import * as vscode from 'vscode';
import { AIService } from '../services/aiService';

export async function generateCodeCommand(aiService: AIService) {
    const prompt = await vscode.window.showInputBox({
        prompt: 'Describe the code you want to generate',
        placeHolder: 'e.g., Create a function to sort an array',
        ignoreFocusOut: true
    });

    if (!prompt) {
        return;
    }

    const editor = vscode.window.activeTextEditor;
    const language = editor?.document.languageId || 'python';

    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: 'Generating code...',
        cancellable: false
    }, async (_progress: vscode.Progress<{ increment: number; message: string }>) => {
        const response = await aiService.generateCode(prompt, language);
        
        if (response.success && editor) {
            const code = response.data.code;
            const position = editor.selection.active;
            await editor.edit((editBuilder: vscode.TextEditorEdit) => {
                editBuilder.insert(position, code);
            });
            vscode.window.showInformationMessage(`Code generated using ${response.model_used || 'AI'}`);
        }
    });
}

export async function reviewCodeCommand(aiService: AIService) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showWarningMessage('Please open a file to review');
        return;
    }

    const code = editor.document.getText();
    const language = editor.document.languageId;
    const filePath = editor.document.fileName;

    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: 'Reviewing code...',
        cancellable: false
    }, async (_progress: vscode.Progress<{ increment: number; message: string }>) => {
        const response = await aiService.reviewCode(code, language, filePath);
        
        if (response.success) {
            const review = response.data.review;
            const panel = vscode.window.createWebviewPanel(
                'codeReview',
                'Code Review',
                vscode.ViewColumn.Beside,
                { enableScripts: true }
            );
            
            panel.webview.html = getReviewHtml(review);
        }
    });
}

export async function explainCodeCommand(aiService: AIService) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showWarningMessage('Please select code to explain');
        return;
    }

    const selection = editor.selection;
    const code = editor.document.getText(selection.isEmpty ? undefined : selection);
    const language = editor.document.languageId;

    const prompt = `Explain this ${language} code in detail:\n\n${code}`;

    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: 'Explaining code...',
        cancellable: false
    }, async (_progress: vscode.Progress<{ increment: number; message: string }>) => {
        const response = await aiService.generateCode(prompt, language);
        
        if (response.success) {
            const explanation = response.data.code;
            const panel = vscode.window.createWebviewPanel(
                'codeExplanation',
                'Code Explanation',
                vscode.ViewColumn.Beside,
                { enableScripts: true }
            );
            
            panel.webview.html = getExplanationHtml(explanation);
        }
    });
}

export async function refactorCodeCommand(aiService: AIService) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showWarningMessage('Please select code to refactor');
        return;
    }

    const selection = editor.selection;
    const code = editor.document.getText(selection);
    const language = editor.document.languageId;

    if (!code) {
        vscode.window.showWarningMessage('Please select code to refactor');
        return;
    }

    const prompt = `Refactor this ${language} code to improve readability and performance:\n\n${code}`;

    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: 'Refactoring code...',
        cancellable: false
    }, async (_progress: vscode.Progress<{ increment: number; message: string }>) => {
        const response = await aiService.generateCode(prompt, language);
        
        if (response.success) {
            const refactoredCode = response.data.code;
            await editor.edit((editBuilder: vscode.TextEditorEdit) => {
                editBuilder.replace(selection, refactoredCode);
            });
            vscode.window.showInformationMessage('Code refactored successfully');
        }
    });
}

export async function designArchitectureCommand(aiService: AIService) {
    const requirements = await vscode.window.showInputBox({
        prompt: 'Describe your project requirements',
        placeHolder: 'e.g., Build a scalable e-commerce platform',
        ignoreFocusOut: true
    });

    if (!requirements) {
        return;
    }

    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: 'Designing architecture...',
        cancellable: false
    }, async (_progress: vscode.Progress<{ increment: number; message: string }>) => {
        const response = await aiService.designArchitecture(requirements);
        
        if (response.success) {
            const architecture = response.data.architecture;
            const panel = vscode.window.createWebviewPanel(
                'architecture',
                'Architecture Design',
                vscode.ViewColumn.One,
                { enableScripts: true }
            );
            
            panel.webview.html = getArchitectureHtml(architecture);
        }
    });
}

export async function analyzeRepositoryCommand(aiService: AIService) {
    const repoUrl = await vscode.window.showInputBox({
        prompt: 'Enter GitHub repository URL',
        placeHolder: 'https://github.com/user/repo',
        ignoreFocusOut: true
    });

    if (!repoUrl) {
        return;
    }

    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: 'Analyzing repository...',
        cancellable: false
    }, async (_progress: vscode.Progress<{ increment: number; message: string }>) => {
        const response = await aiService.analyzeRepository(repoUrl);
        
        if (response.success) {
            const analysis = response.data.analysis;
            const panel = vscode.window.createWebviewPanel(
                'repoAnalysis',
                'Repository Analysis',
                vscode.ViewColumn.One,
                { enableScripts: true }
            );
            
            panel.webview.html = getAnalysisHtml(analysis);
        }
    });
}

export async function selectModelCommand(aiService: AIService) {
    const models = await aiService.getAvailableModels();

    const selected = await vscode.window.showQuickPick(models, {
        placeHolder: 'Select AI model',
        ignoreFocusOut: true
    });

    if (selected) {
        const config = vscode.workspace.getConfiguration('unified-ai');
        await config.update('defaultModel', selected, vscode.ConfigurationTarget.Global);
        vscode.window.showInformationMessage(`Switched to ${selected} model`);
    }
}

export async function codesOpenedCommand(_aiService: AIService) {
    const openedEditors = vscode.window.visibleTextEditors;
    const openedFiles = openedEditors.map((editor: vscode.TextEditor) => editor.document.uri.fsPath);

    if (openedFiles.length === 0) {
        vscode.window.showInformationMessage('No files are currently opened');
        return;
    }

    const fileList = openedFiles.map((file: string, index: number) =>
        `${index + 1}. ${vscode.workspace.asRelativePath(file)}`
    ).join('\n');

    const panel = vscode.window.createWebviewPanel(
        'openedFiles',
        'Opened Files',
        vscode.ViewColumn.Beside,
        { enableScripts: true }
    );

    panel.webview.html = getOpenedFilesHtml(fileList, openedFiles.length);
}

// HTML templates
function getReviewHtml(review: string): string {
    return `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; line-height: 1.6; }
                h1 { color: #0066cc; }
                pre { background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
            </style>
        </head>
        <body>
            <h1>Code Review</h1>
            <pre>${escapeHtml(review)}</pre>
        </body>
        </html>
    `;
}

function getExplanationHtml(explanation: string): string {
    return `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; line-height: 1.6; }
                h1 { color: #0066cc; }
                pre { background: #f4f4f4; padding: 10px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>Code Explanation</h1>
            <pre>${escapeHtml(explanation)}</pre>
        </body>
        </html>
    `;
}

function getArchitectureHtml(architecture: string): string {
    return `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; line-height: 1.6; }
                h1 { color: #0066cc; }
                pre { background: #f4f4f4; padding: 10px; border-radius: 5px; white-space: pre-wrap; }
            </style>
        </head>
        <body>
            <h1>Architecture Design</h1>
            <pre>${escapeHtml(architecture)}</pre>
        </body>
        </html>
    `;
}

function getAnalysisHtml(analysis: string): string {
    return `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; line-height: 1.6; }
                h1 { color: #0066cc; }
                pre { background: #f4f4f4; padding: 10px; border-radius: 5px; white-space: pre-wrap; }
            </style>
        </head>
        <body>
            <h1>Repository Analysis</h1>
            <pre>${escapeHtml(analysis)}</pre>
        </body>
        </html>
    `;
}

function getOpenedFilesHtml(fileList: string, count: number): string {
    return `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; line-height: 1.6; }
                h1 { color: #0066cc; }
                pre { background: #f4f4f4; padding: 15px; border-radius: 5px; white-space: pre-wrap; font-family: monospace; }
                .count { color: #666; font-size: 0.9em; margin-bottom: 10px; }
            </style>
        </head>
        <body>
            <h1>Opened Files</h1>
            <div class="count">Total: ${count} file(s)</div>
            <pre>${escapeHtml(fileList)}</pre>
        </body>
        </html>
    `;
}

function escapeHtml(text: string): string {
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
