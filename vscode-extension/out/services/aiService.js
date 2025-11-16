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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AIService = void 0;
const axios_1 = __importDefault(require("axios"));
const vscode = __importStar(require("vscode"));
class AIService {
    constructor() {
        this.config = vscode.workspace.getConfiguration('unified-ai');
        const apiUrl = this.config.get('apiUrl', 'http://localhost:8000');
        const apiKey = this.config.get('apiKey', '');
        this.client = axios_1.default.create({
            baseURL: apiUrl,
            timeout: 60000,
            headers: apiKey ? { 'Authorization': `Bearer ${apiKey}` } : {}
        });
    }
    async generateCode(prompt, language, context) {
        try {
            const response = await this.client.post('/api/v1/generate', {
                prompt,
                language,
                context,
                temperature: this.config.get('temperature', 0.2),
                max_tokens: this.config.get('maxTokens', 4096),
                model: this.config.get('defaultModel', 'claude')
            });
            return response.data;
        }
        catch (error) {
            return this.handleError(error);
        }
    }
    async reviewCode(code, language, filePath) {
        try {
            const response = await this.client.post('/api/v1/review', {
                code,
                language,
                file_path: filePath,
                model: this.config.get('defaultModel', 'claude')
            });
            return response.data;
        }
        catch (error) {
            return this.handleError(error);
        }
    }
    async designArchitecture(requirements) {
        try {
            const response = await this.client.post('/api/v1/architecture', {
                requirements,
                model: this.config.get('defaultModel', 'claude')
            });
            return response.data;
        }
        catch (error) {
            return this.handleError(error);
        }
    }
    async analyzeRepository(repoUrl, analysisType = 'structure') {
        try {
            const response = await this.client.post('/api/v1/github/analyze', {
                repo_url: repoUrl,
                analysis_type: analysisType
            });
            return response.data;
        }
        catch (error) {
            return this.handleError(error);
        }
    }
    async getAvailableModels() {
        try {
            const response = await this.client.get('/api/v1/models');
            return response.data.available_models || [];
        }
        catch (error) {
            console.error('Error fetching models:', error);
            return ['claude', 'openai', 'gemini'];
        }
    }
    handleError(error) {
        let message = 'An error occurred';
        if (error instanceof Error) {
            message = error.message;
        }
        else if (typeof error === 'object' && error !== null) {
            const err = error;
            message = err.response?.data?.detail || err.message || message;
        }
        vscode.window.showErrorMessage(`AI Assistant Error: ${message}`);
        return {
            success: false,
            data: {},
            message
        };
    }
}
exports.AIService = AIService;
//# sourceMappingURL=aiService.js.map