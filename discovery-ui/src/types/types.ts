export interface ToolCall {
  id: string;
  name: string;
  args: any;
  result?: string;
  status: "pending" | "completed" | "error";
}

export interface SubAgent {
  id: string;
  name: string;
  subAgentName: string;
  input: any;
  output?: any;
  status: "pending" | "active" | "completed" | "error";
}

export interface FileItem {
  path: string;
  content: string;
}

export interface TodoItem {
  id: string;
  content: string;
  status: "pending" | "in_progress" | "completed";
  createdAt?: Date;
  updatedAt?: Date;
}

export interface Thread {
  id: string;
  title: string;
  createdAt: Date;
  updatedAt: Date;
}

// Message types for LangGraph SDK compatibility
export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  createdAt?: Date;
  parts?: any[];
}

// Extended message type for deep agent features
export interface ExtendedMessage extends ChatMessage {
  toolCalls?: ToolCall[];
  subAgents?: SubAgent[];
  files?: FileItem[];
}

// State type for LangGraph agent
export interface AgentState {
  messages: ChatMessage[];
  todos: TodoItem[];
  files: Record<string, string>;
  subAgents: SubAgent[];
}

// UI-specific types
export interface VisibilityType {
  type: "public" | "private";
}

export interface ChatModel {
  id: string;
  name: string;
  provider: string;
}

// Error types
export interface ChatError {
  message: string;
  code?: string;
  details?: any;
}

// Streaming types
export interface StreamEvent {
  type: "message" | "tool_call" | "subagent" | "file" | "error";
  data: any;
}

// Sidebar types
export interface SidebarState {
  isOpen: boolean;
  activeTab: "tasks" | "files" | "history";
}

// Artifact types (preserved from existing)
export interface Artifact {
  id: string;
  title: string;
  content: string;
  type: "text" | "code" | "image" | "sheet";
  createdAt: Date;
}
