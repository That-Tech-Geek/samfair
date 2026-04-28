export interface AedtTool {
  name: string;
  endpoint: string;
}

export interface AuditResult {
  attribute: string;
  group: string;
  selection_rate: number;
  impact_ratio: number;
  flagged: boolean;
  size: number;
}

export interface PpnlOutput {
  rule: string;
  group_impacted: string;
  surrogate_accuracy: number;
  feature_contributions: Record<string, number>;
}

export interface AuditResponse {
  seed: number;
  audit_results: AuditResult[];
  ppnl: PpnlOutput | null;
  report_path: string;
}

export interface User {
  uid: string;
  email: string | null;
  displayName: string | null;
  isEvaluator?: boolean;
}
