import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'nodejs';

/**
 * Enhanced chat API route with improved LangGraph integration
 * Proxies requests to the LangGraph API server with better error handling
 */
export async function POST(req: NextRequest) {
  try {
    // Validate request method
    if (req.method !== 'POST') {
      return new NextResponse('Method not allowed', { status: 405 });
    }

    // Parse and validate payload
    let payload;
    try {
      payload = await req.json();
    } catch (parseError) {
      console.error('📡 Invalid JSON payload:', parseError);
      return new NextResponse(
        `data: {"type":"error","message":"Invalid JSON payload"}\ndata: [DONE]\n\n`,
        {
          status: 400,
          headers: {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
          },
        }
      );
    }

    // Validate required fields
    if (!payload.id || !payload.messages) {
      console.error('📡 Missing required fields:', { id: payload.id, messages: payload.messages });
      return new NextResponse(
        `data: {"type":"error","message":"Missing required fields: id and messages"}\ndata: [DONE]\n\n`,
        {
          status: 400,
          headers: {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
          },
        }
      );
    }

    // Format payload for LangGraph API
    const formattedPayload = {
      id: payload.id,
      messages: payload.messages,
      // Include additional metadata if provided
      ...(payload.selectedChatModel && { selectedChatModel: payload.selectedChatModel }),
      ...(payload.selectedVisibilityType && { selectedVisibilityType: payload.selectedVisibilityType }),
    };

    const backendUrl = process.env.DISCOVERY_AGENT_URL ?? 'http://localhost:8080';
    const endpoint = `${backendUrl}/chat/stream`;

    console.log('📡 Proxying to LangGraph API:', endpoint);

    try {
      const upstream = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'user-agent': 'Discovery-UI/1.0',
        },
        body: JSON.stringify(formattedPayload),
        // Add timeout for better error handling
        signal: AbortSignal.timeout(30000), // 30 second timeout
      });

      if (!upstream.ok) {
        console.error('📡 Backend error:', {
          status: upstream.status,
          statusText: upstream.statusText,
          url: endpoint
        });

        let errorText = 'Unknown backend error';
        try {
          errorText = await upstream.text();
          console.error('📡 Backend error body:', errorText);
        } catch (textError) {
          console.error('📡 Could not read error response:', textError);
        }

        // Return structured error in Data Stream format
        const errorResponse = `data: {"type":"error","message":"LangGraph API error: ${upstream.status} ${upstream.statusText}","details":"${errorText.replace(/"/g, '\\"')}"}\ndata: [DONE]\n\n`;
        return new NextResponse(errorResponse, {
          status: upstream.status,
          headers: {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
          },
        });
      }

      console.log('📡 LangGraph API response successful');

      // Return the streaming response with proper headers
      return new NextResponse(upstream.body, {
        status: upstream.status,
        statusText: upstream.statusText,
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
          // Forward relevant headers from backend
          ...Object.fromEntries(
            Array.from(upstream.headers.entries()).filter(([key]) =>
              ['content-type', 'x-ratelimit-limit', 'x-ratelimit-remaining'].includes(key.toLowerCase())
            )
          ),
        },
      });

    } catch (fetchError) {
      console.error('📡 Fetch error:', fetchError);

      let errorMessage = 'Backend unavailable';
      let statusCode = 503;

      if (fetchError instanceof Error) {
        if (fetchError.name === 'AbortError') {
          errorMessage = 'Request timeout - LangGraph API took too long to respond';
          statusCode = 504;
        } else if (fetchError.message.includes('ECONNREFUSED')) {
          errorMessage = 'Cannot connect to LangGraph API server';
        } else {
          errorMessage = `Backend error: ${fetchError.message}`;
        }
      }

      const errorResponse = `data: {"type":"error","message":"${errorMessage}"}\ndata: [DONE]\n\n`;
      return new NextResponse(errorResponse, {
        status: statusCode,
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
      });
    }

  } catch (error) {
    console.error('📡 API Route error:', error);

    const errorMessage = error instanceof Error ? error.message : 'Internal server error';
    const errorResponse = `data: {"type":"error","message":"API Route error: ${errorMessage}"}\ndata: [DONE]\n\n`;

    return new NextResponse(errorResponse, {
      status: 500,
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });
  }
}
