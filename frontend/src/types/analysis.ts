export interface AgentIssue {
  severity: string;
  title: string;
  reason: string;
}

export interface AgentSuggestion {
  priority: number;
  action: string;
}

export interface AgentResult {
  score: number;
  issues: AgentIssue[];
  suggestions: AgentSuggestion[];
}

export interface AggregatedResult {
  overall_score: number;
  issues: AgentIssue[];
  suggestions: AgentSuggestion[];
}

export interface Visualizations {
  layout_overlay: string;
  ocr_overlay: string;
  issue_overlay: string;
}

export interface AnalysisResponse {

  aggregated_result: AggregatedResult;

  visualizations: Visualizations;

  agent_outputs: {

    layout: AgentResult;

    typography: AgentResult;

    color: AgentResult;

    ux: AgentResult;
  };
}