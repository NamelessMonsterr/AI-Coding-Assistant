"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const aiService_1 = require("./services/aiService");
const ChatViewProvider_1 = require("./views/ChatViewProvider");
const commands_1 = require("./commands");
let aiService;
let chatViewProvider;
function activate(context) {
    console.log('Unified AI Coding Assistant is now active!');
    // Initialize AI service
    aiService = new aiService_1.AIService();
    // Register chat view provider
    chatViewProvider = new ChatViewProvider_1.ChatViewProvider(context.extensionUri, aiService);
    context.subscriptions.push(vscode.window.registerWebviewViewProvider('unified-ai.chatView', chatViewProvider));
    // Register commands
    context.subscriptions.push(vscode.commands.registerCommand('unified-ai.openChat', () => {
        vscode.commands.executeCommand('unified-ai.chatView.focus');
    }), vscode.commands.registerCommand('unified-ai.clearChat', () => {
        chatViewProvider.clearChat();
    }), vscode.commands.registerCommand('unified-ai.generateCode', () => (0, commands_1.generateCodeCommand)(aiService)), vscode.commands.registerCommand('unified-ai.reviewCode', () => (0, commands_1.reviewCodeCommand)(aiService)), vscode.commands.registerCommand('unified-ai.explainCode', () => (0, commands_1.explainCodeCommand)(aiService)), vscode.commands.registerCommand('unified-ai.refactorCode', () => (0, commands_1.refactorCodeCommand)(aiService)), vscode.commands.registerCommand('unified-ai.designArchitecture', () => (0, commands_1.designArchitectureCommand)(aiService)), vscode.commands.registerCommand('unified-ai.analyzeRepository', () => (0, commands_1.analyzeRepositoryCommand)(aiService)), vscode.commands.registerCommand('unified-ai.selectModel', () => (0, commands_1.selectModelCommand)(aiService)), vscode.commands.registerCommand('unified-ai.codesOpened', () => (0, commands_1.codesOpenedCommand)(aiService)));
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
function deactivate() {
    console.log('Unified AI Coding Assistant is now deactivated');
}
//# sourceMappingURL=extension.js.map