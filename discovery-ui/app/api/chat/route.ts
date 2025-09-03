import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'nodejs';

export async function POST(req: NextRequest) {
  try {
    const payload = await req.json();

    // The payload should now be in the correct format from the transport
    // { id, messages: [...], selectedChatModel, selectedVisibilityType }
    const formattedPayload = {
      id: payload.id,
      messages: payload.messages,
    };

    const backendUrl = process.env.DISCOVERY_AGENT_URL ?? 'http://localhost:8080';

    try {
      const upstream = await fetch(`${backendUrl}/chat/stream`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(formattedPayload),
      });

      if (!upstream.ok) {
        console.error('📡 Backend error:', upstream.status, upstream.statusText);
        const errorText = await upstream.text();
        console.error('📡 Backend error body:', errorText);

        // Return error in Data Stream format
        const errorResponse = `data: {"type":"error","message":"Backend error: ${upstream.status} ${upstream.statusText}"}\ndata: [DONE]\n\n`;
        return new NextResponse(errorResponse, {
          status: upstream.status,
          headers: {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
          },
        });
      }

      // Return the streaming response with proper Data Stream headers
      return new NextResponse(upstream.body, {
        status: upstream.status,
        statusText: upstream.statusText,
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
          ...Object.fromEntries(upstream.headers.entries()),
        },
      });
    } catch (fetchError) {
      console.error('📡 Fetch error:', fetchError);
      const errorMessage = fetchError instanceof Error ? fetchError.message : 'Unknown error';
      const errorResponse = `data: {"type":"error","message":"Backend unavailable: ${errorMessage}"}\ndata: [DONE]\n\n`;
      return new NextResponse(errorResponse, {
        status: 503,
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
      });
    }
  } catch (error) {
    console.error('📡 API Route error:', error);
    return new NextResponse(JSON.stringify({ error: 'Internal server error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
