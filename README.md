# 🎨 Design Evaluation AI

An AI-powered multimodal design critique platform that analyzes UI screenshots, posters, landing pages, dashboards, and product interfaces using Computer Vision, OCR, Layout Analysis, Multi-Agent Reasoning, and LLM-based Design Evaluation.

## Overview

Design Evaluation AI automatically reviews visual designs and provides professional feedback similar to what a Senior Product Designer, UX Researcher, or Design Reviewer would provide.

The system combines:

- Computer Vision
- OCR
- Layout Analysis
- Multi-Agent Evaluation
- LLM-based Design Critique
- Design Memory Retrieval
- Reflection & Self-Critique

to generate actionable design feedback.

The platform is intended for:

- UI/UX Designers
- Product Designers
- Frontend Developers
- Startup Founders
- Design Teams
- Student Design Clubs
- Hackathon Participants

## Problem Statement

Design reviews are often:

- Expensive
- Slow
- Subjective
- Not always available

Students, developers, and startups frequently need quick feedback on:

- Landing Pages
- Posters
- Mobile Screens
- Dashboards
- Product Interfaces

without waiting for a human reviewer.

This project attempts to provide an automated design review assistant using multimodal AI.

## Why This Project?

Traditional image captioning models only describe interfaces.

They do not answer:

- Is hierarchy good?
- Is spacing consistent?
- Is typography readable?
- Is the CTA discoverable?
- Is the design cluttered?
- Are colors accessible?

This project focuses specifically on design quality evaluation.

## Core Features

### Visual Analysis

Extracts:

- Dominant Colors
- Layout Blocks
- Component Regions
- Edge Density
- White Space Ratio
- Text Density

### OCR Analysis

Detects:

- Headings
- Body Text
- Labels
- CTA Text

using EasyOCR.

### Layout Analysis

Measures:

- Alignment
- White Space
- Visual Balance
- Section Structure
- Clutter

### Multi-Agent Architecture

Specialized agents independently evaluate:

#### Layout Agent

Analyzes:

- Alignment
- Spacing
- Balance
- White Space

#### Typography Agent

Analyzes:

- Readability
- Hierarchy
- Information Density
- CTA Visibility

#### Color Agent

Analyzes:

- Contrast
- Accessibility
- Harmony
- Saturation

#### UX Agent

Analyzes:

- Navigation
- CTA Discoverability
- Scanability
- Cognitive Load

---

### Evaluator Agent

Reviews all agent outputs.

Detects:

- Generic Feedback
- Repeated Insights
- Weak Suggestions
- Hallucinated Critique

### Reflection Agent

Improves critique quality.

Transforms generic feedback into:

- Specific
- Actionable
- Professional recommendations

### Design Memory

Stores previous reviews.

Enables:

- Similarity Retrieval
- Historical Comparison
- Future Learning

### Visualization Engine

Generates:

- OCR Overlays
- Layout Block Maps
- Problem Region Highlighting

## High-Level Architecture

```text
User Upload
     │
     ▼
Image Storage
     │
     ▼
Computer Vision Pipeline
     │
     ├── OCR
     ├── Color Analysis
     ├── Layout Detection
     ├── White Space Analysis
     └── Density Analysis
     │
     ▼
Vision Metrics
     │
     ▼
Multi-Agent System
     │
     ├── Layout Agent
     ├── Typography Agent
     ├── Color Agent
     └── UX Agent
     │
     ▼
Evaluator Agent
     │
     ▼
Reflection Agent
     │
     ▼
Vision LLM Review
     │
     ▼
Aggregation Layer
     │
     ▼
Memory Storage
     │
     ▼
Frontend Dashboard
```

## Backend Architecture

### Tech Stack

#### Framework

- FastAPI

#### AI

- Groq API
- Llama 4 Scout

#### Vision

- OpenCV

#### OCR

- EasyOCR

#### Validation

- Pydantic

#### Memory

- Local JSON Storage

## Backend Folder Structure

```text
backend/
│
├── app/
│
├── agents/
│   ├── layout_agent.py
│   ├── typography_agent.py
│   ├── color_agent.py
│   ├── ux_agent.py
│   ├── evaluator_agent.py
│   └── reflection_agent.py
│
├── routes/
│   └── analyze.py
│
├── services/
│   ├── ai_service.py
│   ├── ocr_service.py
│   ├── vision_service.py
│   ├── component_service.py
│   ├── layout_service.py
│   ├── orchestrator_service.py
│   ├── aggregator_service.py
│   ├── memory_service.py
│   ├── retrieval_service.py
│   ├── visualization_service.py
│   ├── issue_visualization_service.py
│   └── agent_utils.py
│
├── schemas/
│   ├── response_schema.py
│   └── agent_schema.py
│
├── prompts/
│   └── critique_prompt.py
│
└── uploads/
```

## File Responsibilities

### analyze.py

Main API endpoint.

Responsibilities:

- Receive image
- Save image
- Trigger analysis pipeline
- Return final response

### ai_service.py

Main multimodal LLM evaluator.

Responsibilities:

- Convert image to Base64
- Send image to LLM
- Merge visual metrics
- Generate final design critique

### ocr_service.py

Extracts text from images using EasyOCR.

Returns:

- Text
- Confidence
- Bounding Boxes

### layout_service.py

Calculates:

- White Space Ratio
- Edge Density
- Spacing Consistency

### component_service.py

Detects layout blocks and UI regions.

### orchestrator_service.py

Controls all agents.

Workflow:

```text
Layout Agent
Typography Agent
Color Agent
UX Agent
      ↓
Evaluator
      ↓
Reflection
      ↓
Aggregation
```

### aggregator_service.py

Combines all agent outputs into a unified review.

### memory_service.py

Stores review history.

### retrieval_service.py

Retrieves similar historical reviews.

## Frontend Architecture

### Tech Stack

- React
- TypeScript
- Tailwind CSS
- Axios
- Vite

## Frontend Structure

```text
frontend/
│
├── src/
│
├── components/
│   ├── UploadSection.tsx
│   ├── ScoreCard.tsx
│   ├── AgentPanel.tsx
│   └── VisualizationPanel.tsx
│
├── services/
│   └── api.ts
│
├── types/
│   └── analysis.ts
│
├── pages/
│
└── App.tsx
```

## Design Decisions

### Why Multi-Agent?

Single prompts tend to:

- Miss issues
- Repeat feedback
- Provide generic critiques

Using specialist agents improves:

- Depth
- Diversity
- Coverage

### Why OCR?

Design quality depends heavily on typography.

Images alone are insufficient.

OCR enables:

- Text Density Analysis
- CTA Detection
- Readability Evaluation

### Why Reflection?

LLM critiques often contain:

- Generic suggestions
- Repeated advice

Reflection improves quality before delivery.

## Research Inspiration

This project draws ideas from:

### Vision-Language Models

- CLIP
- BLIP
- LLaVA
- GPT-4V

### Multi-Agent Reasoning

- AutoGen (Microsoft)
- CAMEL
- CrewAI

### Reflection Systems

- Reflexion
- Self-Refine

### Retrieval-Augmented Systems

- RAG
- Memory-Augmented Agents

### Design Evaluation Research

- Visual Hierarchy Research
- Nielsen UX Heuristics
- Gestalt Principles
- Accessibility Guidelines (WCAG)

## API Endpoint

### Analyze Design

```http
POST /analyze
```

#### Input

```text
multipart/form-data

file=image.png
```

#### Output

```json
{
  "overall_score": 8.2,
  "summary": {},
  "agent_outputs": {},
  "evaluation": {},
  "refined_output": {},
  "visualizations": {}
}
```

## Local Setup

### Clone Repository

```bash
git clone <repo-url>
```

### Backend Setup

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create:

```text
.env
```

Add:

```env
GROQ_API_KEY=your_key_here
```

Run:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## Current Limitations

- Uses heuristic layout detection
- OCR errors affect critique quality
- No true accessibility engine
- No Figma integration
- No component-level understanding
- No user personalization

## Future Scope

### Figma Plugin

Analyze designs directly inside Figma.

### Accessibility Engine

WCAG compliance scoring.

### Component Detection

Detect:

- Buttons
- Forms
- Cards
- Navbars

using object detection.

### Design Benchmarking

Compare against:

- Apple
- Stripe
- Linear
- Airbnb
- Notion

design standards.

### Learning Feedback Loop

Store user ratings and improve critique quality over time.

### Design Copilot

Interactive AI assistant capable of:

- Explaining issues
- Generating redesign ideas
- Producing improved layouts

## Potential Impact

This project demonstrates:

- Computer Vision
- OCR
- LLM Engineering
- Multi-Agent Systems
- Retrieval Systems
- Full Stack Development
- AI Product Design

in a single end-to-end application.

It serves as both a practical design-review tool and a showcase of modern multimodal AI system architecture.
