# Grand Chat Tutorial

A full-stack real-time chat application built with Django, WebSocket, and a modern frontend. This project serves as a boilerplate and educational template for building real-time messaging systems.

## 📁 Project Structure

- `/app/` — Django backend application  
- `/chat/` — WebSocket logic (rooms, connections, messaging)  
- `/frontend/` — Frontend app   
- `/nginx/` — Nginx configuration files (optional)  
- `Dockerfile` — Backend Docker build instructions  
- `docker-compose.yml` — Multi-container app orchestration  
- `pyproject.toml`, `poetry.lock` — Python dependencies via Poetry  
- `manage.py` — Django project entry point  

## 🚀 Quick Start (with Docker)

1. Make sure Docker and Docker Compose are installed.
2. Clone this repository:

   ```bash
   git clone https://github.com/Volodymyr-tech/grand-chat-tutorial.git
   cd grand-chat-tutorial

## ✨ Features

Real-time messaging with WebSocket support

Clean separation of frontend and backend logic

Dockerized environment for consistent development

Scalable architecture with room for extension

Optional Nginx configuration for production

Authentication-ready 

## 🛠 Technologies Used

Backend: Django, ASGI, WebSockets

Frontend: React, TypeScript 

Database: PostgreSQL 

DevOps: Docker, Docker Compose, Nginx

## 🧱 How to Extend the Project

Add login/registration system

Store chat history in a database

Support private and group chats

Add features like typing indicators and read receipts

Improve mobile responsiveness and UI/UX

Integrate AI agents (e.g. GPT bots via LangChain)

## 📌 Use Cases

Educational sandbox for real-time app development

Boilerplate for SaaS chat systems

Template for building a scalable messaging backend

Playground for integrating AI into real-time communication
