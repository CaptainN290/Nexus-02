# Overview

This is a Discord moderation bot built with discord.py. The bot provides comprehensive server moderation and management capabilities including member management, channel controls, role management, information commands, and utility features. It uses a command prefix "n/" and is designed to help Discord server administrators effectively manage their communities with 20+ commands.

# Recent Changes

**October 27, 2025**: Major feature expansion
- Added 16 new commands across 5 categories (moderation, channel management, role management, information, and utility)
- Implemented comprehensive help command with categorized display
- Added error handling for message deletion in say/announce commands
- Fixed type hints for optional member parameters
- All commands include proper permission checks and error handling

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Bot Framework
- **Technology**: discord.py library with commands extension
- **Command System**: Prefix-based commands using "n/" prefix
- **Intents**: Default intents with message_content enabled to read and process command messages
- **Rationale**: discord.py is the standard Python library for Discord bot development, providing robust event handling and command processing capabilities

## Command Structure
- **Pattern**: Command decorator-based architecture (@bot.command())
- **Help System**: Custom help command implementation using Discord embeds
- **Rationale**: Decorators provide clean, modular command organization; custom help command allows branded, organized command documentation

## Authentication & Permissions
- **Token Management**: Environment variable-based token storage (secure approach)
- **Permission Model**: Leverages Discord's built-in permission system for moderation commands
- **Rationale**: Environment variables prevent token exposure in code; Discord's native permissions ensure proper access control

## Response Format
- **Embeds**: Rich Discord embeds for command responses and help documentation
- **Color Coding**: Blue color scheme for informational messages
- **Rationale**: Embeds provide better visual organization and professional appearance compared to plain text messages

## Feature Categories

### Moderation Commands
- **Member Management**: Kick, ban, unban, timeout, warn, mute/unmute capabilities
- **Message Management**: Bulk message deletion (clear command) with 1-100 message limit
- **Rationale**: Core moderation toolkit for disciplinary actions and member management

### Channel Management
- **Channel Controls**: Slowmode (0-21600 seconds), lock/unlock functionality
- **Rationale**: Provides fine-grained control over channel behavior and accessibility

### Role Management
- **Role Assignment**: Add/remove roles from members
- **Rationale**: Streamlines role management for administrators

### Information Commands
- **User Information**: Display user profile details (ID, join date, roles, avatar)
- **Server Information**: Show server statistics (member count, creation date, owner)
- **Bot Status**: Ping command for latency monitoring
- **Rationale**: Provides quick access to important server and member information

### Utility Commands
- **Messaging**: Say command for bot announcements
- **Polls**: Interactive poll creation with emoji reactions (up to 10 options)
- **Announcements**: Formatted announcement embeds
- **Rationale**: Adds engagement and communication tools for server management

# External Dependencies

## Core Dependencies
- **discord.py**: Python library for Discord API integration
  - Provides bot framework, command processing, and event handling
  - Enables interaction with Discord servers, channels, and members

## Runtime Requirements
- **Python 3.8+**: Required for discord.py compatibility
- **Environment Variables**: Secure storage for Discord bot token

## Discord API
- **Authentication**: Bot token authentication
- **Permissions Required**: 
  - Read messages
  - Send messages
  - Manage messages (for clear command)
  - Kick/ban members
  - Manage roles (for mute functionality)
  - Manage channels (for lock/slowmode)
  - Moderate members (for timeout)