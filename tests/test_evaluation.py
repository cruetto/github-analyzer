"""
GitHub AI Analyzer - Test Evaluation Report Generator
=====================================================
Generates comprehensive test evaluation reports with:
- Test results tables
- Performance metrics
- Error analysis
- NLP quality metrics (BLEU, ROUGE-L)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict


@dataclass
class EvaluationMetrics:
    """Evaluation metrics for a single test"""
    query_id: int
    query: str
    entity_extraction_success: bool
    extracted_repo: str
    expected_repo: str
    entity_accuracy: float
    api_success: bool
    analysis_generated: bool
    response_length: int
    contains_expected_language: bool
    contains_repo_name: bool
    execution_time_ms: float
    

@dataclass
class NLPMetrics:
    """NLP quality metrics"""
    bleu_score: float
    rouge_l_score: float
    semantic_similarity: float
    entity_precision: float
    entity_recall: float
    entity_f1: float


class TestEvaluationReport:
    """Generate comprehensive test evaluation reports"""
    
    def __init__(self):
        self.metrics: List[EvaluationMetrics] = []
        self.nlp_metrics: Dict[int, NLPMetrics] = {}
        self.manual_evaluations: List[Dict] = []
        
    def add_metric(self, metric: EvaluationMetrics):
        """Add a test metric"""
        self.metrics.append(metric)
    
    def add_nlp_metric(self, query_id: int, metrics: NLPMetrics):
        """Add NLP metrics for a query"""
        self.nlp_metrics[query_id] = metrics
    
    def add_manual_evaluation(self, evaluation: Dict):
        """Add manual evaluation result"""
        self.manual_evaluations.append(evaluation)
    
    def generate_summary_table(self) -> str:
        """Generate summary statistics table"""
        if not self.metrics:
            return "No metrics available"
        
        total = len(self.metrics)
        entity_success = sum(1 for m in self.metrics if m.entity_extraction_success)
        api_success = sum(1 for m in self.metrics if m.api_success)
        analysis_success = sum(1 for m in self.metrics if m.analysis_generated)
        
        avg_entity_accuracy = sum(m.entity_accuracy for m in self.metrics) / total
        avg_response_length = sum(m.response_length for m in self.metrics) / total
        avg_execution_time = sum(m.execution_time_ms for m in self.metrics) / total
        
        table = """
┌─────────────────────────────────────────────────────────────┐
│                    TEST SUMMARY STATISTICS                    │
├─────────────────────────────────────────────────────────────┤
│ Metric                          │ Value                      │
├─────────────────────────────────────────────────────────────┤
│ Total Test Queries              │ {total:<25}│
│ Entity Extraction Success       │ {entity_success}/{total} ({entity_pct:.1%})          │
│ API Integration Success         │ {api_success}/{total} ({api_pct:.1%})          │
│ Analysis Generation Success     │ {analysis_success}/{total} ({analysis_pct:.1%})          │
│ Avg Entity Extraction Accuracy  │ {avg_entity_accuracy:.2%}                        │
│ Avg Response Length (chars)      │ {avg_response_length:<25.0f}│
│ Avg Execution Time (ms)         │ {avg_execution_time:<25.0f}│
└─────────────────────────────────────────────────────────────┘
""".format(
            total=total,
            entity_success=entity_success,
            entity_pct=entity_success/total,
            api_success=api_success,
            api_pct=api_success/total,
            analysis_success=analysis_success,
            analysis_pct=analysis_success/total,
            avg_entity_accuracy=avg_entity_accuracy,
            avg_response_length=avg_response_length,
            avg_execution_time=avg_execution_time
        )
        return table
    
    def generate_detailed_table(self) -> str:
        """Generate detailed test results table"""
        if not self.metrics:
            return "No metrics available"
        
        header = """
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                              DETAILED TEST RESULTS                                          │
├────┬─────────────────────────┬───────────┬──────────┬──────────┬──────────┬─────────────────┤
│ ID │ Query                   │ Entity OK │ API OK   │ Analysis │ Accuracy │ Repo Extracted  │
├────┼─────────────────────────┼───────────┼──────────┼──────────┼──────────┼─────────────────┤"""
        
        rows = []
        for m in self.metrics:
            query_short = m.query[:23] + ".." if len(m.query) > 23 else m.query
            repo_short = m.extracted_repo[:15] if m.extracted_repo else "None"
            
            entity_status = "✓" if m.entity_extraction_success else "✗"
            api_status = "✓" if m.api_success else "✗"
            analysis_status = "✓" if m.analysis_generated else "✗"
            
            row = "│{id:<4}│{query:<25}│{entity:<11}│{api:<10}│{analysis:<10}│{accuracy:<10.2f}│{repo:<17}│".format(
                id=m.query_id,
                query=query_short,
                entity=entity_status,
                api=api_status,
                analysis=analysis_status,
                accuracy=m.entity_accuracy,
                repo=repo_short
            )
            rows.append(row)
        
        footer = "└────┴─────────────────────────┴───────────┴──────────┴──────────┴──────────┴─────────────────┘"
        
        return header + "\n" + "\n".join(rows) + "\n" + footer
    
    def generate_nlp_metrics_table(self) -> str:
        """Generate NLP metrics table"""
        if not self.nlp_metrics:
            return "No NLP metrics available"
        
        header = """
┌───────────────────────────────────────────────────────────────────────────────┐
│                           NLP QUALITY METRICS                                 │
├────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────────────┤
│ ID │ BLEU     │ ROUGE-L  │ Sem Sim  │ Prec     │ Recall   │ F1 Score         │
├────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────────────┤"""
        
        rows = []
        for query_id, metrics in sorted(self.nlp_metrics.items()):
            row = "│{id:<4}│{bleu:<10.3f}│{rouge:<10.3f}│{sem:<10.3f}│{prec:<10.3f}│{recall:<10.3f}│{f1:<18.3f}│".format(
                id=query_id,
                bleu=metrics.bleu_score,
                rouge=metrics.rouge_l_score,
                sem=metrics.semantic_similarity,
                prec=metrics.entity_precision,
                recall=metrics.entity_recall,
                f1=metrics.entity_f1
            )
            rows.append(row)
        
        footer = "└────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────────────┘"
        
        return header + "\n" + "\n".join(rows) + "\n" + footer
    
    def generate_manual_evaluation_table(self) -> str:
        """Generate manual evaluation results table"""
        if not self.manual_evaluations:
            return "No manual evaluations available"
        
        header = """
┌──────────────────────────────────────────────────────────────────────────────────┐
│                           MANUAL EVALUATION RESULTS                              │
├────┬─────────────────────────┬──────────────────┬──────────┬─────────────────────┤
│ ID │ Query                   │ Evaluation Type  │ Score    │ Notes               │
├────┼─────────────────────────┼──────────────────┼──────────┼─────────────────────┤"""
        
        rows = []
        for i, eval_data in enumerate(self.manual_evaluations, 1):
            query_short = eval_data.get('query', '')[:23] + ".." if len(eval_data.get('query', '')) > 23 else eval_data.get('query', '')
            eval_type = eval_data.get('type', 'N/A')[:16]
            score = f"{eval_data.get('score', 0):.2f}/1.00"
            notes = eval_data.get('notes', '')[:19]
            
            row = "│{id:<4}│{query:<25}│{type:<18}│{score:<10}│{notes:<21}│".format(
                id=i,
                query=query_short,
                type=eval_type,
                score=score,
                notes=notes
            )
            rows.append(row)
        
        footer = "└────┴─────────────────────────┴──────────────────┴──────────┴─────────────────────┘"
        
        return header + "\n" + "\n".join(rows) + "\n" + footer
    
    def generate_error_analysis(self) -> str:
        """Generate error analysis section"""
        errors = []
        
        # Entity extraction errors
        entity_failures = [m for m in self.metrics if not m.entity_extraction_success]
        if entity_failures:
            errors.append("ENTITY EXTRACTION FAILURES:")
            for m in entity_failures:
                errors.append(f"  Query {m.query_id}: '{m.query}'")
                errors.append(f"    Expected: {m.expected_repo}, Got: {m.extracted_repo or 'None'}")
            errors.append("")
        
        # API failures
        api_failures = [m for m in self.metrics if not m.api_success]
        if api_failures:
            errors.append("API INTEGRATION FAILURES:")
            for m in api_failures:
                errors.append(f"  Query {m.query_id}: '{m.query}'")
            errors.append("")
        
        # Analysis failures
        analysis_failures = [m for m in self.metrics if not m.analysis_generated]
        if analysis_failures:
            errors.append("ANALYSIS GENERATION FAILURES:")
            for m in analysis_failures:
                errors.append(f"  Query {m.query_id}: '{m.query}'")
                errors.append(f"    Response length: {m.response_length}")
            errors.append("")
        
        if not errors:
            return "No errors detected in test suite."
        
        return "\n".join(errors)
    
    def generate_full_report(self) -> str:
        """Generate complete evaluation report"""
        report = []
        report.append("=" * 90)
        report.append("GITHUB AI ANALYZER - TEST EVALUATION REPORT")
        report.append("=" * 90)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        report.append(self.generate_summary_table())
        report.append("")
        
        # Detailed Results
        report.append(self.generate_detailed_table())
        report.append("")
        
        # NLP Metrics
        report.append(self.generate_nlp_metrics_table())
        report.append("")
        
        # Manual Evaluations
        report.append(self.generate_manual_evaluation_table())
        report.append("")
        
        # Error Analysis
        report.append("ERROR ANALYSIS")
        report.append("-" * 40)
        report.append(self.generate_error_analysis())
        report.append("")
        
        # Conclusions
        report.append("CONCLUSIONS")
        report.append("-" * 40)
        report.append(self._generate_conclusions())
        
        return "\n".join(report)
    
    def _generate_conclusions(self) -> str:
        """Generate conclusions based on metrics"""
        if not self.metrics:
            return "No data available for conclusions."
        
        total = len(self.metrics)
        entity_success_rate = sum(1 for m in self.metrics if m.entity_extraction_success) / total
        api_success_rate = sum(1 for m in self.metrics if m.api_success) / total
        analysis_success_rate = sum(1 for m in self.metrics if m.analysis_generated) / total
        
        conclusions = []
        
        # Entity Extraction Assessment
        if entity_success_rate >= 0.8:
            conclusions.append("✓ Entity Extraction: EXCELLENT (>80% success rate)")
        elif entity_success_rate >= 0.6:
            conclusions.append("△ Entity Extraction: GOOD (60-80% success rate)")
        else:
            conclusions.append("✗ Entity Extraction: NEEDS IMPROVEMENT (<60% success rate)")
        
        # API Integration Assessment
        if api_success_rate >= 0.9:
            conclusions.append("✓ API Integration: EXCELLENT (>90% success rate)")
        elif api_success_rate >= 0.7:
            conclusions.append("△ API Integration: GOOD (70-90% success rate)")
        else:
            conclusions.append("✗ API Integration: NEEDS IMPROVEMENT (<70% success rate)")
        
        # Analysis Generation Assessment
        if analysis_success_rate >= 0.9:
            conclusions.append("✓ Analysis Generation: EXCELLENT (>90% success rate)")
        elif analysis_success_rate >= 0.7:
            conclusions.append("△ Analysis Generation: GOOD (70-90% success rate)")
        else:
            conclusions.append("✗ Analysis Generation: NEEDS IMPROVEMENT (<70% success rate)")
        
        # NLP Quality Assessment
        if self.nlp_metrics:
            avg_bleu = sum(m.bleu_score for m in self.nlp_metrics.values()) / len(self.nlp_metrics)
            avg_rouge = sum(m.rouge_l_score for m in self.nlp_metrics.values()) / len(self.nlp_metrics)
            
            if avg_bleu >= 0.5 and avg_rouge >= 0.5:
                conclusions.append("✓ NLP Quality: GOOD (BLEU & ROUGE-L > 0.5)")
            elif avg_bleu >= 0.3 and avg_rouge >= 0.3:
                conclusions.append("△ NLP Quality: ACCEPTABLE (BLEU & ROUGE-L > 0.3)")
            else:
                conclusions.append("✗ NLP Quality: NEEDS IMPROVEMENT")
        
        return "\n".join(conclusions)
    
    def save_report(self, filepath: str = "TEST_REPORT.txt"):
        """Save report to file"""
        report = self.generate_full_report()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report saved to: {filepath}")
    
    def save_json(self, filepath: str = "test_results.json"):
        """Save metrics as JSON"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "metrics": [asdict(m) for m in self.metrics],
            "nlp_metrics": {str(k): asdict(v) for k, v in self.nlp_metrics.items()},
            "manual_evaluations": self.manual_evaluations
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"JSON results saved to: {filepath}")


def create_sample_report():
    """Create a sample evaluation report for demonstration"""
    report = TestEvaluationReport()
    
    # Sample metrics for 5 test queries
    sample_data = [
        (1, "Analyze the tensorflow repository", "tensorflow", "tensorflow", True, True, True, 2500, True),
        (2, "What does the React library do?", "react", "react", True, True, True, 2800, True),
        (3, "Tell me about the flask web framework", "flask", "flask", True, True, True, 2200, True),
        (4, "Show me information about pandas data analysis library", "pandas", "pandas", True, True, True, 2600, True),
        (5, "How does the express.js framework work?", "express", "express", True, True, True, 2400, True),
    ]
    
    for query_id, query, expected, extracted, entity_ok, api_ok, analysis_ok, resp_len, lang_ok in sample_data:
        metric = EvaluationMetrics(
            query_id=query_id,
            query=query,
            entity_extraction_success=entity_ok,
            extracted_repo=extracted,
            expected_repo=expected,
            entity_accuracy=1.0 if extracted.lower() == expected.lower() else 0.8,
            api_success=api_ok,
            analysis_generated=analysis_ok,
            response_length=resp_len,
            contains_expected_language=lang_ok,
            contains_repo_name=True,
            execution_time_ms=1500.0 + query_id * 100
        )
        report.add_metric(metric)
    
    # Sample NLP metrics
    for query_id in range(1, 6):
        nlp = NLPMetrics(
            bleu_score=0.65 + (query_id * 0.02),
            rouge_l_score=0.70 + (query_id * 0.01),
            semantic_similarity=0.75 + (query_id * 0.01),
            entity_precision=1.0,
            entity_recall=1.0,
            entity_f1=1.0
        )
        report.add_nlp_metric(query_id, nlp)
    
    # Sample manual evaluations
    manual_evals = [
        {"query": "Analyze the tensorflow repository", "type": "Semantic Similarity", "score": 0.85, "notes": "Good coverage"},
        {"query": "What does the React library do?", "type": "Response Structure", "score": 0.90, "notes": "Well organized"},
        {"query": "Tell me about flask", "type": "Completeness", "score": 0.88, "notes": "All elements present"},
    ]
    for eval_data in manual_evals:
        report.add_manual_evaluation(eval_data)
    
    return report


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║          GitHub AI Analyzer - Test Evaluation Report Generator       ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Create sample report
    report = create_sample_report()
    
    # Print report to console
    print(report.generate_full_report())
    
    # Save report to files
    report.save_report("TEST_REPORT.txt")
    report.save_json("test_results.json")
    
    print("\n✓ Report generation complete!")