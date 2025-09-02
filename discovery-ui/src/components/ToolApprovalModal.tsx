"use client";
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertTriangle, Wrench, X } from "lucide-react";

interface ToolCall {
  id: string;
  name: string;
  args: Record<string, any>;
}

interface ToolApprovalModalProps {
  toolCall: ToolCall | null;
  isOpen: boolean;
  onApprove: (customArgs?: Record<string, any>) => void;
  onReject: () => void;
  onClose: () => void;
}

export function ToolApprovalModal({
  toolCall,
  isOpen,
  onApprove,
  onReject,
  onClose
}: ToolApprovalModalProps) {
  const [customArgs, setCustomArgs] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleApprove = async () => {
    setIsLoading(true);
    try {
      let parsedArgs: Record<string, any> | undefined;
      if (customArgs.trim()) {
        try {
          parsedArgs = JSON.parse(customArgs);
        } catch (e) {
          alert('Invalid JSON in custom arguments');
          setIsLoading(false);
          return;
        }
      }
      await onApprove(parsedArgs);
      onClose();
    } catch (error) {
      console.error('Error approving tool:', error);
      alert('Failed to approve tool. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReject = async () => {
    setIsLoading(true);
    try {
      await onReject();
      onClose();
    } catch (error) {
      console.error('Error rejecting tool:', error);
      alert('Failed to reject tool. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen || !toolCall) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-[500px] max-h-[80vh] overflow-y-auto">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-amber-500" />
              <CardTitle>Tool Approval Required</CardTitle>
            </div>
            <Button variant="ghost" size="icon" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>
          <CardDescription>
            The agent wants to execute a tool that requires your approval.
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-4">
          <div className="flex items-center gap-2">
            <Wrench className="h-4 w-4 text-blue-500" />
            <span className="font-medium">Tool: {toolCall.name}</span>
            <Badge variant="secondary">Requires Approval</Badge>
          </div>

          <div>
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Tool Arguments:
            </label>
            <pre className="mt-1 p-3 bg-gray-50 dark:bg-gray-800 rounded-md text-sm overflow-x-auto">
              {JSON.stringify(toolCall.args, null, 2)}
            </pre>
          </div>

          <div>
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Custom Arguments (JSON - optional):
            </label>
            <Textarea
              value={customArgs}
              onChange={(e) => setCustomArgs(e.target.value)}
              placeholder='{"custom_param": "value"}'
              className="mt-1 font-mono text-sm"
              rows={3}
            />
            <p className="text-xs text-gray-500 mt-1">
              Leave empty to use the default arguments above, or provide custom JSON to override them.
            </p>
          </div>
        </CardContent>

        <CardFooter className="flex gap-2">
          <Button
            variant="outline"
            onClick={handleReject}
            disabled={isLoading}
            className="flex-1"
          >
            Reject
          </Button>
          <Button
            onClick={handleApprove}
            disabled={isLoading}
            className="flex-1"
          >
            {isLoading ? 'Processing...' : 'Approve'}
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
