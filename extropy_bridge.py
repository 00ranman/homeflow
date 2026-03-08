#!/usr/bin/env python3
"""
Extropy Engine Bridge for HomeFlow

This module replaces the old unified_integration.py with a bridge that
connects directly to the deployed Extropy Engine HomeFlow service
(TypeScript/Express on port 4015) running at extropyengine.com.

The standalone Python HomeFlow service can run in two modes:
  1. PROXY mode: All API calls forwarded to the deployed service
  2. HYBRID mode: Local SQLite for offline, syncs to deployed when online

Environment variables:
  EXTROPY_HOMEFLOW_URL  - Deployed HomeFlow API (default: https://extropyengine.com/homeflow)
  EXTROPY_MODE          - 'proxy' or 'hybrid' (default: hybrid)
  EXTROPY_API_KEY       - API key for authentication with deployed service

Ref: https://github.com/00ranman/extropy-engine/issues/5
"""

import os
import json
import logging
import asyncio
from typing import Dict, Any, Optional

import aiohttp

logger = logging.getLogger(__name__)

# ── Configuration ──────────────────────────────────────────────────────────
EXTROPY_HOMEFLOW_URL = os.getenv('EXTROPY_HOMEFLOW_URL', 'https://extropyengine.com/homeflow')
EXTROPY_MODE = os.getenv('EXTROPY_MODE', 'hybrid')
EXTROPY_API_KEY = os.getenv('EXTROPY_API_KEY', '')

# Deployed service endpoints (TypeScript service on port 4015)
ENDPOINTS = {
    'health': f'{EXTROPY_HOMEFLOW_URL}/health',
    'households': f'{EXTROPY_HOMEFLOW_URL}/api/v1/households',
    'devices': f'{EXTROPY_HOMEFLOW_URL}/api/v1/devices',
    'entropy': f'{EXTROPY_HOMEFLOW_URL}/api/v1/entropy',
    'interop': f'{EXTROPY_HOMEFLOW_URL}/api/v1/interop',
    # These will be available after extropy-engine#5 is implemented:
    'inventory': f'{EXTROPY_HOMEFLOW_URL}/api/v1/inventory',
    'chores': f'{EXTROPY_HOMEFLOW_URL}/api/v1/chores',
    'meals': f'{EXTROPY_HOMEFLOW_URL}/api/v1/meals',
    'health_profiles': f'{EXTROPY_HOMEFLOW_URL}/api/v1/health',
    'shopping': f'{EXTROPY_HOMEFLOW_URL}/api/v1/shopping',
    'xp': f'{EXTROPY_HOMEFLOW_URL}/api/v1/xp',
}

# ── Core Bridge Class ──────────────────────────────────────────────────────

class ExtropyBridge:
    """Bridges local HomeFlow operations to the deployed Extropy Engine."""

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.connected = False
        self.mode = EXTROPY_MODE
        self._headers = {
            'Content-Type': 'application/json',
            'X-Service': 'homeflow-standalone',
        }
        if EXTROPY_API_KEY:
            self._headers['Authorization'] = f'Bearer {EXTROPY_API_KEY}'

    async def connect(self) -> bool:
        """Initialize connection to deployed service."""
        try:
            self.session = aiohttp.ClientSession(headers=self._headers)
            async with self.session.get(ENDPOINTS['health']) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self.connected = True
                    logger.info(f"Connected to Extropy Engine HomeFlow: {data.get('version', 'unknown')}")
                    return True
            self.connected = False
            logger.warning('Extropy Engine HomeFlow service not reachable, running in local mode')
            return False
        except Exception as e:
            self.connected = False
            logger.warning(f'Failed to connect to Extropy Engine: {e}')
            return False

    async def close(self):
        if self.session:
            await self.session.close()

    # ── Proxy Methods ──────────────────────────────────────────────────────

    async def proxy_request(self, method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """Forward a request to the deployed service."""
        if not self.session or not self.connected:
            return {'error': 'Not connected to Extropy Engine', 'fallback': 'local'}

        try:
            url = f'{EXTROPY_HOMEFLOW_URL}{endpoint}'
            async with self.session.request(method, url, json=data) as resp:
                return await resp.json()
        except Exception as e:
            logger.error(f'Proxy request failed: {e}')
            return {'error': str(e), 'fallback': 'local'}

    # ── Entropy Event Emission ─────────────────────────────────────────────

    async def emit_entropy_event(self, event_type: str, payload: Dict) -> Optional[str]:
        """Emit an entropy reduction event to the deployed service's event webhook."""
        result = await self.proxy_request('POST', '/events', {
            'type': event_type,
            'source': 'homeflow-standalone',
            'payload': payload,
        })
        return result.get('eventId')

    # ── Inventory Bridge ───────────────────────────────────────────────────

    async def sync_inventory_item(self, item_data: Dict) -> Optional[str]:
        """Sync a local inventory item to the deployed service."""
        result = await self.proxy_request('POST', '/api/v1/inventory', item_data)
        if 'id' in result:
            # Emit entropy event for inventory organization
            await self.emit_entropy_event('INVENTORY_UPDATED', {
                'itemId': result['id'],
                'action': item_data.get('action', 'add'),
                'deltaS': 0.1,  # Base entropy reduction for inventory management
            })
        return result.get('id')

    # ── Chore/Task Bridge ──────────────────────────────────────────────────

    async def sync_task_completion(self, completion_data: Dict) -> Optional[str]:
        """Sync a task completion to earn XP via the deployed service."""
        result = await self.proxy_request('POST', '/api/v1/chores/complete', completion_data)
        return result.get('xp_transaction_id')

    # ── Meal Bridge ────────────────────────────────────────────────────────

    async def sync_meal_prep(self, meal_data: Dict) -> Optional[str]:
        """Sync meal preparation data for entropy measurement."""
        result = await self.proxy_request('POST', '/api/v1/meals/prep-session', meal_data)
        return result.get('xp_transaction_id')

    # ── Health Bridge ──────────────────────────────────────────────────────

    async def sync_health_activity(self, health_data: Dict) -> Optional[str]:
        """Sync health optimization activity."""
        result = await self.proxy_request('POST', '/api/v1/health/track-activity', health_data)
        return result.get('xp_transaction_id')

    # ── Cross-domain Interop ───────────────────────────────────────────────

    async def get_interop_manifest(self) -> Dict:
        """Get the interop manifest from the deployed service."""
        return await self.proxy_request('GET', '/api/v1/interop/manifest')

    async def request_cross_domain_entropy(self, target_app: str, data: Dict) -> Dict:
        """Request cross-domain entropy aggregation with another ecosystem app."""
        return await self.proxy_request('POST', f'/api/v1/interop/cross-entropy/{target_app}', data)


# ── Module-level singleton ─────────────────────────────────────────────────
bridge = ExtropyBridge()


# ── Drop-in replacements for unified_integration.py functions ──────────────
# These maintain backward compatibility with homeflow_service.py

async def initialize_integration(email: str, password: str = None, token: str = None) -> bool:
    """Initialize connection to the deployed Extropy Engine."""
    if token:
        bridge._headers['Authorization'] = f'Bearer {token}'
    return await bridge.connect()


async def track_chore_completion(chore_data: Dict) -> Optional[str]:
    """Track chore completion via deployed service."""
    if bridge.connected:
        return await bridge.sync_task_completion(chore_data)
    # Fallback: just log locally
    logger.info(f"Local chore tracking (offline): {chore_data.get('name', 'unknown')}")
    return None


async def track_inventory_management(inventory_data: Dict) -> Optional[str]:
    """Track inventory management via deployed service."""
    if bridge.connected:
        return await bridge.sync_inventory_item(inventory_data)
    logger.info(f"Local inventory tracking (offline): {inventory_data.get('action', 'unknown')}")
    return None


async def track_meal_preparation(meal_data: Dict) -> Optional[str]:
    """Track meal preparation via deployed service."""
    if bridge.connected:
        return await bridge.sync_meal_prep(meal_data)
    logger.info(f"Local meal tracking (offline): {meal_data.get('meal_name', 'unknown')}")
    return None


async def track_health_optimization(health_data: Dict) -> Optional[str]:
    """Track health optimization via deployed service."""
    if bridge.connected:
        return await bridge.sync_health_activity(health_data)
    logger.info(f"Local health tracking (offline): {health_data.get('activity_type', 'unknown')}")
    return None


async def create_household_task_in_signalflow(task_data: Dict) -> Optional[str]:
    """Create task via deployed service's SignalFlow integration."""
    if bridge.connected:
        result = await bridge.proxy_request('POST', '/api/v1/chores/create-signalflow', task_data)
        return result.get('signalflow_task_id')
    return None


def get_integration_status() -> Dict[str, Any]:
    """Get current integration status."""
    return {
        'authenticated': bridge.connected,
        'mode': bridge.mode,
        'deployed_url': EXTROPY_HOMEFLOW_URL,
        'user': None,  # Will be populated after auth
        'household_analytics': {
            'connected': bridge.connected,
            'service': 'extropy-engine/homeflow@4015',
        },
    }


# Legacy alias
integration = bridge
