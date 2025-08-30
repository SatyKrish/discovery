#!/usr/bin/env python3
"""
Web Search MCP Server - Mock web search functionality
"""

import asyncio
import sys
import os
import json
from typing import List, Dict, Any

# Add the parent directory to the path so we can import base_server
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_server import BaseMCPServer

class WebSearchServer(BaseMCPServer):
    """MCP Server for web search functionality"""

    def __init__(self):
        super().__init__("web-search-server", "1.0.0")

    def _setup_tools(self):
        """Setup the web search tools"""

        @self.server.tool()
        async def web_search(query: str, max_results: int = 5) -> Dict[str, Any]:
            """Search the web for information.

            This is a mock implementation that returns simulated search results.
            In a real implementation, this would connect to actual search APIs.

            Args:
                query: The search query
                max_results: Maximum number of results to return (default: 5)

            Returns:
                Dictionary containing search results
            """
            # Mock search results - in real implementation, this would call actual search APIs
            mock_results = self._generate_mock_results(query, max_results)

            return {
                "query": query,
                "total_results": len(mock_results),
                "results": mock_results,
                "search_engine": "mock-search",
                "timestamp": "2025-01-01T12:00:00Z"
            }

        @self.server.tool()
        async def search_news(query: str, days_back: int = 7) -> Dict[str, Any]:
            """Search for recent news articles.

            Args:
                query: The news search query
                days_back: How many days back to search (default: 7)

            Returns:
                Dictionary containing news search results
            """
            mock_news = self._generate_mock_news(query, days_back)

            return {
                "query": query,
                "days_back": days_back,
                "total_results": len(mock_news),
                "results": mock_news,
                "source": "mock-news-api",
                "timestamp": "2025-01-01T12:00:00Z"
            }

        @self.server.tool()
        async def search_images(query: str, max_results: int = 10) -> Dict[str, Any]:
            """Search for images related to the query.

            Args:
                query: The image search query
                max_results: Maximum number of image results to return (default: 10)

            Returns:
                Dictionary containing image search results
            """
            mock_images = self._generate_mock_images(query, max_results)

            return {
                "query": query,
                "total_results": len(mock_images),
                "results": mock_images,
                "source": "mock-image-search",
                "timestamp": "2025-01-01T12:00:00Z"
            }

    def _generate_mock_results(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Generate mock search results"""
        base_results = [
            {
                "title": f"Understanding {query}",
                "url": f"https://example.com/understanding-{query.lower().replace(' ', '-')}",
                "snippet": f"Learn everything about {query} in this comprehensive guide.",
                "domain": "example.com"
            },
            {
                "title": f"{query} - Wikipedia",
                "url": f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}",
                "snippet": f"{query} is a topic of great interest in various fields.",
                "domain": "wikipedia.org"
            },
            {
                "title": f"Latest {query} Developments",
                "url": f"https://news.example.com/{query.lower().replace(' ', '-')}-developments",
                "snippet": f"Recent developments in {query} have been significant.",
                "domain": "news.example.com"
            },
            {
                "title": f"{query} Best Practices",
                "url": f"https://blog.example.com/{query.lower().replace(' ', '-')}-best-practices",
                "snippet": f"Follow these best practices for {query}.",
                "domain": "blog.example.com"
            },
            {
                "title": f"{query} Tutorial",
                "url": f"https://tutorial.example.com/{query.lower().replace(' ', '-')}",
                "snippet": f"Step-by-step tutorial on {query}.",
                "domain": "tutorial.example.com"
            }
        ]

        return base_results[:max_results]

    def _generate_mock_news(self, query: str, days_back: int) -> List[Dict[str, Any]]:
        """Generate mock news results"""
        return [
            {
                "title": f"Breaking: New {query} Discovery",
                "url": f"https://news.example.com/breaking-{query.lower().replace(' ', '-')}",
                "snippet": f"Scientists have made a groundbreaking discovery related to {query}.",
                "published_date": "2025-01-01T10:00:00Z",
                "source": "Science News"
            },
            {
                "title": f"{query} Market Trends",
                "url": f"https://business.example.com/{query.lower().replace(' ', '-')}-market",
                "snippet": f"Analysis of current market trends in {query}.",
                "published_date": "2025-01-01T08:30:00Z",
                "source": "Business Daily"
            }
        ]

    def _generate_mock_images(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Generate mock image results"""
        return [
            {
                "title": f"{query} illustration",
                "url": f"https://images.example.com/{query.lower().replace(' ', '-')}-1.jpg",
                "thumbnail_url": f"https://images.example.com/thumb/{query.lower().replace(' ', '-')}-1.jpg",
                "width": 800,
                "height": 600,
                "format": "jpg"
            },
            {
                "title": f"{query} diagram",
                "url": f"https://images.example.com/{query.lower().replace(' ', '-')}-2.jpg",
                "thumbnail_url": f"https://images.example.com/thumb/{query.lower().replace(' ', '-')}-2.jpg",
                "width": 1024,
                "height": 768,
                "format": "jpg"
            }
        ][:max_results]


def main():
    """Main entry point for the web search server"""
    server = WebSearchServer()
    server.run()


if __name__ == "__main__":
    main()
