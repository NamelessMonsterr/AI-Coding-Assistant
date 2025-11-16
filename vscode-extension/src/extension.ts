import * as vscode from 'vscode';
import { AIService } from './services/aiService';
import { ChatViewProvider } from './views/ChatViewProvider';
import {
    generateCodeCommand,
    reviewCodeCommand,
    explainCodeCommand,
    refactorCodeCommand,
    designArchitectureCommand,
    analyzeRepositoryCommand,
    selectModelCommand,
    codesOpenedCommand
} from './commands';

let aiService: AIService;
let chatViewProvider: ChatViewProvider;

export function activate(context: vscode.ExtensionContext) {
    console.log('Unified AI Coding Assistant is now active!');

    // Initialize AI service
    aiService = new AIService();

    // Register chat view provider
    chatViewProvider = new ChatViewProvider(context.extensionUri, aiService);
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider('unified-ai.chatView', chatViewProvider)
    );

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('unified-ai.openChat', () => {
            vscode.commands.executeCommand('unified-ai.chatView.focus');
        }),
        vscode.commands.registerCommand('unified-ai.clearChat', () => {
            chatViewProvider.clearChat();
        }),
        vscode.commands.registerCommand('unified-ai.generateCode', () => generateCodeCommand(aiService)),
        vscode.commands.registerCommand('unified-ai.reviewCode', () => reviewCodeCommand(aiService)),
        vscode.commands.registerCommand('unified-ai.explainCode', () => explainCodeCommand(aiService)),
        vscode.commands.registerCommand('unified-ai.refactorCode', () => refactorCodeCommand(aiService)),
        vscode.commands.registerCommand('unified-ai.designArchitecture', () => designArchitectureCommand(aiService)),
        vscode.commands.registerCommand('unified-ai.analyzeRepository', () => analyzeRepositoryCommand(aiService)),
        vscode.commands.registerCommand('unified-ai.selectModel', () => selectModelCommand(aiService)),
        vscode.commands.registerCommand('unified-ai.codesOpened', () => codesOpenedCommand(aiService))
    );

    // Status bar item
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.text = `$(sparkle) AI Assistant`;
    statusBarItem.tooltip = 'Unified AI Coding Assistant - Click to open chat';
    statusBarItem.command = 'unified-ai.openChat';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    // Show welcome message
    vscode.window.showInformationMessage('✅ AI Assistant ready! Click the status bar or sidebar to start chatting.');
}

export function deactivate() {
    console.log('Unified AI Coding Assistant is now deactivated');
}
