'use client';

import { memo } from 'react';
import { Button } from './ui/button';
import { Lightbulb, Search, Code, TrendingUp, BookOpen, Zap } from 'lucide-react';

interface SuggestedActionsProps {
  onActionClick: (action: string) => void;
}

const suggestedActions = [
  {
    icon: Search,
    text: "Research the latest AI advancements",
    prompt: "Research and summarize the latest advancements in artificial intelligence and machine learning"
  },
  {
    icon: Code,
    text: "Debug a technical issue",
    prompt: "Help me debug a complex technical issue. I need to identify the root cause and find a solution."
  },
  {
    icon: TrendingUp,
    text: "Analyze industry trends",
    prompt: "Analyze current trends in technology and provide insights about future developments"
  },
  {
    icon: BookOpen,
    text: "Learn a new concept",
    prompt: "Explain a complex technical concept in simple terms and provide practical examples"
  },
  {
    icon: Zap,
    text: "Optimize performance",
    prompt: "Help me optimize the performance of my system/application. Identify bottlenecks and suggest improvements."
  },
  {
    icon: Lightbulb,
    text: "Brainstorm solutions",
    prompt: "Help me brainstorm creative solutions for a challenging problem. Consider multiple approaches and their trade-offs."
  }
];

function PureSuggestedActions({ onActionClick }: SuggestedActionsProps) {
  return (
    <div className="grid grid-cols-2 gap-4 p-4">
      {suggestedActions.map((action, index) => {
        const IconComponent = action.icon;
        return (
          <Button
            key={index}
            variant="outline"
            className="h-auto p-5 text-left hover:bg-gradient-to-r hover:from-primary/5 hover:to-primary/10 hover:shadow-md hover:border-primary/20 transition-all duration-300 justify-start rounded-xl shadow-sm border-border/50 bg-card/50 backdrop-blur-sm"
            onClick={() => onActionClick(action.prompt)}
          >
            <div className="flex items-center gap-4 w-full">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-primary/20 to-primary/10 flex items-center justify-center shadow-sm">
                <IconComponent className="w-4.5 h-4.5 text-primary" />
              </div>
              <span className="text-sm text-foreground flex-1 leading-relaxed font-medium">
                {action.text}
              </span>
            </div>
          </Button>
        );
      })}
    </div>
  );
}

export const SuggestedActions = memo(PureSuggestedActions);
