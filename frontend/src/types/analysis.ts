export interface AgentIssue {
  severity: string;
  title: string;
  reason: string;
}

export interface AgentSuggestion {
  priority: number;
  action: string;
}

export interface AggregatedResult {
  overall_score: number;
  issues: AgentIssue[];
  suggestions: AgentSuggestion[];
}

export interface AnalysisResponse {
  aggregated_result: AggregatedResult;
}