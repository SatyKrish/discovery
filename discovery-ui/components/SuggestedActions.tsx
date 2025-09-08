'use client';

import React from 'react';
import { Button } from './ui/button';
import { Search, Code, TrendingUp, BookOpen, Zap, Lightbulb } from 'lucide-react';

interface SuggestedActionsProps {
  onActionClick: (prompt: string) => void;
}

const suggestedActions = [
  {
    icon: Search,
    text: "Research AI advancements",
    prompt: "Research the latest advancements in artificial intelligence and machine learning, and summarize the key developments from the past year."
  },
  {
    icon: Code,
    text: "Debug technical issues",
    prompt: "Help me debug a complex technical issue. I need to identify the root cause and find a solution. Please ask me for specific details about the problem."
  },
  {
    icon: TrendingUp,
    text: "Analyze industry trends",
    prompt: "Analyze current trends in technology and provide insights about future developments. Focus on emerging technologies and their potential impact."
  },
  {
    icon: BookOpen,
    text: "Learn new concepts",
    prompt: "Explain a complex technical concept in simple terms and provide practical examples. I'll tell you what concept I want to learn about."
  },
  {
    icon: Zap,
    text: "Optimize performance",
    prompt: "Help me optimize the performance of my system or application. I need to identify bottlenecks and suggest improvements."
  },
  {
    icon: Lightbulb,
    text: "Brainstorm solutions",
    prompt: "Help me brainstorm creative solutions for a challenging problem. Consider multiple approaches and their trade-offs."
  }
];

export const SuggestedActions: React.FC<SuggestedActionsProps> = ({ onActionClick }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full">
      {suggestedActions.map((action, index) => {
        const IconComponent = action.icon;
        return (
          <Button
            key={index}
            variant="outline"
            className="h-auto p-4 text-left hover:bg-muted/50 hover:border-primary/20 transition-all duration-200 justify-start rounded-lg shadow-sm"
            onClick={() => onActionClick(action.prompt)}
          >
            <div className="flex items-start gap-3 w-full">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center mt-0.5">
                <IconComponent className="w-4 h-4 text-primary" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="font-medium text-sm text-foreground mb-1">
                  {action.text}
                </div>
                <div className="text-xs text-muted-foreground line-clamp-2">
                  {action.prompt.length > 100 ? `${action.prompt.substring(0, 100)}...` : action.prompt}
                </div>
              </div>
            </div>
          </Button>
        );
      })}
    </div>
  );
};
