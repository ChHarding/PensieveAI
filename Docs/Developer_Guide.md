# PensieveAI Developer's Guide

This document is a technical reference for developers tasked with maintaining or enhancing **PensieveAI**. It includes an overview, technical architecture, implementation details, known issues, and suggestions for future expansions.

---

## Table of Contents
1. [Overview](#overview)
2. [Technical Flow](#technical-flow)
3. [Installation, Deployment, and Admin Details](#installation-deployment-and-admin-details)
4. [User Interaction and Code Flow](#user-interaction-and-code-flow)
5. [Data Types and Structures](#data-types-and-structures)
6. [Known Issues](#known-issues)
7. [Future Work](#future-work)
8. [Ongoing Maintenance and Development Guidelines](#ongoing-maintenance-and-development-guidelines)

---

## Overview

**PensieveAI** is a web-based platform designed to automate thematic analysis of qualitative textual data. By leveraging OpenAI's GPT-4o mini API, the platform identifies themes, descriptions, and relevant excerpts, saving researchers time and effort. The different types of text data used to analyse with this tool are interview transcripts, focus-group transcripts, open-ended survey feedback, customer reviews, etc.

### Problem Solved
Manual thematic analysis is time-intensive, prone to human error, and challenging for novice researchers. PensieveAI provides an automated starting point with a preliminary thematic analysis, saving significant time and effort.

### Key Features
- Password-protected access using a single passcode.
- Upload and process multiple file formats: `.pdf`, `.docx`, and `.txt`.
- Option to provide user-defined instructions for customized analysis.
- Integration with OpenAI GPT API for thematic analysis.
- Display results in the UI and allow downloading as PDF reports.

### Target Users
- **Social Science Researchers**: Sociologists, anthropologists, and educators.
- **UX Researchers**: Professionals analyzing user interviews and focus groups.
- **Market Researchers**: Teams reviewing consumer feedback or focus groups.
- **Novice Researchers**: Students and beginners in qualitative research.
- **Businesses**: Organizations analyzing feedback or employee interviews.

---

## Technical Flow

