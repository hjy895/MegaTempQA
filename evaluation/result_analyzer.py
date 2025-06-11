"""
Results analysis and reporting
"""

import pandas as pd
import numpy as np
from pathlib import Path

class ResultAnalyzer:
    """Analyzes and reports evaluation results"""
    
    def __init__(self):
        pass
    
    def generate_report(self, results_df: pd.DataFrame, output_dir: Path):
        """Generate comprehensive evaluation report"""
        print("\n📊 Generating evaluation report...")
        
        # Main results table
        self._print_results_table(results_df)
        
        # Analysis
        analysis = self._analyze_results(results_df)
        self._print_analysis(analysis)
        
        # Save detailed report
        self._save_report(results_df, analysis, output_dir)
    
    def _print_results_table(self, results_df: pd.DataFrame):
        """Print main results table"""
        print("\n" + "="*90)
        print("📊 MegaTempQA Evaluation Results")
        print("="*90)
        
        # Group by model and shots
        table_stats = results_df.groupby(['model', 'shots']).agg({
            'precision': 'mean',
            'recall': 'mean',
            'f1': 'mean',
            'containment': 'mean',
            'exact_match': 'mean'
        }).round(3)
        
        # Print header
        print(f"{'Model':<30} {'Shots':<6} {'Precision':<10} {'Recall':<10} {'F1':<10} {'Containment':<12} {'EM':<10}")
        print("-" * 88)
        
        # Print results
        for (model, shots) in table_stats.index:
            model_short = model.split('/')[-1][:25]
            row = table_stats.loc[(model, shots)]
            print(f"{model_short:<30} {shots:<6} {row['precision']:<10.3f} {row['recall']:<10.3f} "
                  f"{row['f1']:<10.3f} {row['containment']:<12.3f} {row['exact_match']:<10.3f}")
    
    def _analyze_results(self, results_df: pd.DataFrame) -> dict:
        """Analyze results and extract insights"""
        analysis = {}
        
        # Best configurations
        model_stats = results_df.groupby(['model', 'shots'])['f1'].mean().reset_index()
        model_stats = model_stats.sort_values('f1', ascending=False)
        analysis['best_configs'] = model_stats.head(10).to_dict('records')
        
        # Few-shot improvements
        improvements = []
        for model in results_df['model'].unique():
            model_data = results_df[results_df['model'] == model]
            shots_data = model_data.groupby('shots')['f1'].mean()
            
            if 0 in shots_data.index and len(shots_data) > 1:
                zero_shot = shots_data[0]
                best_shot = shots_data.max()
                improvement = best_shot - zero_shot
                improvements.append({
                    'model': model,
                    'zero_shot_f1': zero_shot,
                    'best_f1': best_shot,
                    'improvement': improvement
                })
        
        improvements = sorted(improvements, key=lambda x: x['improvement'], reverse=True)
        analysis['improvements'] = improvements[:5]
        
        # Overall statistics
        overall_stats = results_df.groupby('shots').agg({
            'f1': ['mean', 'std'],
            'exact_match': ['mean', 'std'],
            'precision': ['mean', 'std'],
            'recall': ['mean', 'std']
        }).round(3)
        
        analysis['overall_stats'] = overall_stats
        
        # Performance by question type
        qtype_stats = results_df.groupby('question_type').agg({
            'f1': 'mean',
            'exact_match': 'mean'
        }).round(3).sort_values('f1', ascending=False)
        
        analysis['question_type_performance'] = qtype_stats
        
        return analysis
    
    def _print_analysis(self, analysis: dict):
        """Print analysis insights"""
        print(f"\n## 📈 Analysis")
        print("-" * 50)
        
        # Top configurations
        print("🏆 Top 5 configurations:")
        for i, config in enumerate(analysis['best_configs'][:5]):
            model_short = config['model'].split('/')[-1][:20]
            print(f"  {i+1}. {model_short} ({config['shots']}-shot): F1={config['f1']:.3f}")
        
        # Few-shot improvements
        if analysis['improvements']:
            print(f"\n📈 Few-shot learning improvements:")
            for imp in analysis['improvements']:
                model_short = imp['model'].split('/')[-1][:20]
                print(f"  {model_short}: {imp['zero_shot_f1']:.3f} → {imp['best_f1']:.3f} "
                      f"(+{imp['improvement']:.3f})")
        
        # Question type performance
        print(f"\n📊 Performance by question type:")
        qtype_perf = analysis['question_type_performance']
        for qtype in qtype_perf.head(5).index:
            f1 = qtype_perf.loc[qtype, 'f1']
            em = qtype_perf.loc[qtype, 'exact_match']
            print(f"  {qtype}: F1={f1:.3f}, EM={em:.3f}")
        
        # Overall trends
        print(f"\n📈 Performance by shot count:")
        overall = analysis['overall_stats']
        for shots in sorted(overall.index):
            f1_mean = overall.loc[shots, ('f1', 'mean')]
            f1_std = overall.loc[shots, ('f1', 'std')]
            print(f"  {shots}-shot: F1={f1_mean:.3f}±{f1_std:.3f}")
    
    def _save_report(self, results_df: pd.DataFrame, analysis: dict, output_dir: Path):
        """Save detailed analysis report"""
        report_file = output_dir / "evaluation_report.txt"
        
        with open(report_file, 'w') as f:
            f.write("MegaTempQA Evaluation Report\n")
            f.write("=" * 40 + "\n\n")
            
            f.write("Dataset Statistics:\n")
            f.write(f"  Total predictions: {len(results_df)}\n")
            f.write(f"  Models evaluated: {len(results_df['model'].unique())}\n")
            f.write(f"  Question types: {len(results_df['question_type'].unique())}\n\n")
            
            f.write("Top Configurations:\n")
            for i, config in enumerate(analysis['best_configs'][:10]):
                f.write(f"  {i+1}. {config['model']} ({config['shots']}-shot): "
                       f"F1={config['f1']:.3f}\n")
            
            f.write("\nFew-shot Improvements:\n")
            for imp in analysis['improvements']:
                f.write(f"  {imp['model']}: {imp['zero_shot_f1']:.3f} → "
                       f"{imp['best_f1']:.3f} (+{imp['improvement']:.3f})\n")
        
        print(f"📄 Report saved to {report_file}")
