import axios from 'axios';
import * as vscode from 'vscode';

export interface AIResponse<T = Record<string, unknown>> {
    success: boolean;
    data: T;
    message?: string;
    model_used?: string;
}

export interface CodeGenerationData {
    code: string;
}

export interface CodeReviewData {
    review: string;
}

export interface ArchitectureData {
    architecture: string;
}

export interface AnalysisData {
    analysis: string;
}

export class AIService {
    private client: ReturnType<typeof axios.create>;
    private config: vscode.WorkspaceConfiguration;

    constructor() {
        this.config = vscode.workspace.getConfiguration('unified-ai');
        const apiUrl = this.config.get<string>('apiUrl', 'http://localhost:8000');
        const apiKey = this.config.get<string>('apiKey', '');

        this.client = axios.create({
            baseURL: apiUrl,
            timeout: 60000,
            headers: apiKey ? { 'Authorization': `Bearer ${apiKey}` } : {}
        });
    }

    async generateCode(prompt: string, language: string, context?: string): Promise<AIResponse<CodeGenerationData>> {
        try {
            const response = await this.client.post('/api/v1/generate', {
                prompt,
                language,
                context,
                temperature: this.config.get<number>('temperature', 0.2),
                max_tokens: this.config.get<number>('maxTokens', 4096),
                model: this.config.get<string>('defaultModel', 'claude')
            });
            return response.data as AIResponse<CodeGenerationData>;
        } catch (error) {
            return this.handleError<CodeGenerationData>(error);
        }
    }

    async reviewCode(code: string, language: string, filePath?: string): Promise<AIResponse<CodeReviewData>> {
        try {
            const response = await this.client.post('/api/v1/review', {
                code,
                language,
                file_path: filePath,
                model: this.config.get<string>('defaultModel', 'claude')
            });
            return response.data as AIResponse<CodeReviewData>;
        } catch (error) {
            return this.handleError<CodeReviewData>(error);
        }
    }

    async designArchitecture(requirements: string): Promise<AIResponse<ArchitectureData>> {
        try {
            const response = await this.client.post('/api/v1/architecture', {
                requirements,
                model: this.config.get<string>('defaultModel', 'claude')
            });
            return response.data as AIResponse<ArchitectureData>;
        } catch (error) {
            return this.handleError<ArchitectureData>(error);
        }
    }

    async analyzeRepository(repoUrl: string, analysisType: string = 'structure'): Promise<AIResponse<AnalysisData>> {
        try {
            const response = await this.client.post('/api/v1/github/analyze', {
                repo_url: repoUrl,
                analysis_type: analysisType
            });
            return response.data as AIResponse<AnalysisData>;
        } catch (error) {
            return this.handleError<AnalysisData>(error);
        }
    }

    async getAvailableModels(): Promise<string[]> {
        try {
            const response = await this.client.get('/api/v1/models');
            return (response.data as { available_models?: string[] }).available_models || [];
        } catch (error) {
            console.error('Error fetching models:', error);
            return ['claude', 'openai', 'gemini'];
        }
    }

    private handleError<T>(error: unknown): AIResponse<T> {
        let message = 'An error occurred';

        if (error instanceof Error) {
            message = error.message;
        } else if (typeof error === 'object' && error !== null) {
            const err = error as { response?: { data?: { detail?: string } }; message?: string };
            message = err.response?.data?.detail || err.message || message;
        }

        vscode.window.showErrorMessage(`AI Assistant Error: ${message}`);
        return {
            success: false,
            data: {} as T,
            message
        };
    }
}
