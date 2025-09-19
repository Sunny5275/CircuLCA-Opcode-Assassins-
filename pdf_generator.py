import os
import tempfile
from datetime import datetime
from typing import Dict, Any
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.platypus import Image as RLImage
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

class PDFGenerator:
    """Generates PDF reports for LCA results"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.HexColor('#2E86AB')
        )
    
    def generate_report(self, data: Dict[str, Any], calculation_id: str = None) -> Dict[str, str]:
        """
        Generate PDF report from LCA calculation results
        
        Args:
            data: Complete results data from LCA calculation
            calculation_id: Optional unique ID for the calculation
            
        Returns:
            Dictionary containing PDF file path and metadata
        """
        # Create persistent directory for PDF storage
        pdf_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generated_pdfs')
        os.makedirs(pdf_dir, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        calc_id = calculation_id or str(int(datetime.now().timestamp() * 1000))
        
        # Create descriptive filename based on calculation parameters
        enhanced_data = data.get('enhanced_data', {})
        metal_type = enhanced_data.get('metalType', 'unknown').lower()
        production_route = enhanced_data.get('productionRoute', 'unknown').lower()
        
        filename = f"lca_report_{metal_type}_{production_route}_{timestamp}_{calc_id}.pdf"
        pdf_path = os.path.join(pdf_dir, filename)
        
        # Create document
        doc = SimpleDocTemplate(pdf_path, pagesize=A4, topMargin=0.5*inch)
        story = []
        
        # Title
        title = Paragraph("Life Cycle Assessment Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Report metadata
        report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        meta_text = f"<b>Generated:</b> {report_date}<br/><b>Analysis Type:</b> Metallurgy & Mining LCA"
        meta_para = Paragraph(meta_text, self.styles['Normal'])
        story.append(meta_para)
        story.append(Spacer(1, 20))
        
        # Input parameters section
        story.append(Paragraph("Input Parameters", self.heading_style))
        input_data = self._create_input_table(data.get('enhanced_data', {}))
        story.append(input_data)
        story.append(Spacer(1, 15))
        
        # AI enhancements section
        if data.get('enhanced_data', {}).get('ai_estimated_energy') or data.get('enhanced_data', {}).get('ai_estimated_transport'):
            story.append(Paragraph("AI-Enhanced Parameters", self.heading_style))
            ai_text = self._create_ai_enhancement_text(data.get('enhanced_data', {}))
            story.append(Paragraph(ai_text, self.styles['Normal']))
            story.append(Spacer(1, 15))
        
        # Results comparison section
        story.append(Paragraph("Environmental Impact Comparison", self.heading_style))
        results_table = self._create_results_table(data.get('results', {}).get('pathways', []))
        story.append(results_table)
        story.append(Spacer(1, 15))
        
        # Improvements section
        improvements = data.get('results', {}).get('improvements', {})
        if improvements:
            story.append(Paragraph("Circular Economy Benefits", self.heading_style))
            improvements_text = self._create_improvements_text(improvements)
            story.append(Paragraph(improvements_text, self.styles['Normal']))
            story.append(Spacer(1, 15))
        
        # Chart section
        chart_path = self._create_comparison_chart(data.get('results', {}).get('pathways', []))
        if chart_path:
            story.append(Paragraph("Visual Comparison", self.heading_style))
            chart_image = RLImage(chart_path, width=6*inch, height=3*inch)
            story.append(chart_image)
            story.append(Spacer(1, 15))
        
        # Recommendations section
        story.append(Paragraph("Recommendations", self.heading_style))
        recommendations = self._create_recommendations(data)
        story.append(Paragraph(recommendations, self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        # Clean up temporary chart file
        if chart_path and os.path.exists(chart_path):
            os.remove(chart_path)
        
        # Return PDF metadata
        return {
            'pdf_path': pdf_path,
            'filename': filename,
            'calculation_id': calc_id,
            'timestamp': timestamp,
            'metal_type': metal_type,
            'production_route': production_route,
            'file_size': os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 0
        }
    
    def _create_input_table(self, enhanced_data: Dict[str, Any]) -> Table:
        """Create table showing input parameters"""
        data_rows = [
            ['Parameter', 'Value', 'Unit/Type'],
            ['Metal Type', enhanced_data.get('metalType', 'N/A').title(), ''],
            ['Production Route', enhanced_data.get('productionRoute', 'N/A').replace('_', ' ').title(), ''],
            ['Energy Use', f"{enhanced_data.get('energyUse', 0):.1f}", 'kWh/kg'],
            ['Transport Distance', f"{enhanced_data.get('transportDistance', 0):.1f}", 'km'],
            ['End-of-Life Option', enhanced_data.get('endOfLife', 'N/A').title(), '']
        ]
        
        table = Table(data_rows, colWidths=[2.5*inch, 1.5*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _create_results_table(self, pathways: list) -> Table:
        """Create table showing pathway comparison results"""
        data_rows = [['Pathway', 'CO₂ Equivalent (kg/kg)', 'Recycled Content (%)', 'Reuse Potential (%)']]
        
        for pathway in pathways:
            data_rows.append([
                pathway.get('name', ''),
                f"{pathway.get('co2_equivalent', 0):.2f}",
                f"{pathway.get('recycled_content', 0):.1f}",
                f"{pathway.get('reuse_potential', 0):.1f}"
            ])
        
        table = Table(data_rows, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _create_ai_enhancement_text(self, enhanced_data: Dict[str, Any]) -> str:
        """Create text describing AI enhancements"""
        enhancements = []
        
        if enhanced_data.get('ai_estimated_energy'):
            enhancements.append(f"• Energy use estimated at {enhanced_data.get('energyUse', 0):.1f} kWh/kg based on industry standards")
        
        if enhanced_data.get('ai_estimated_transport'):
            enhancements.append(f"• Transport distance estimated at {enhanced_data.get('transportDistance', 0):.1f} km based on typical supply chains")
        
        if enhanced_data.get('process_efficiency'):
            enhancements.append(f"• Process efficiency inferred as {enhanced_data.get('process_efficiency', 0)*100:.1f}%")
        
        return "<br/>".join(enhancements) if enhancements else "No AI enhancements applied."
    
    def _create_improvements_text(self, improvements: Dict[str, Any]) -> str:
        """Create text describing circular economy improvements"""
        co2_reduction = improvements.get('co2_reduction_percent', 0)
        circularity_increase = improvements.get('circularity_increase', 0)
        reuse_improvement = improvements.get('reuse_improvement', 0)
        
        text = f"""<b>Environmental Benefits:</b><br/>
        • CO₂ emissions reduction: {co2_reduction:.1f}%<br/>
        • Increased recycled content: +{circularity_increase:.1f} percentage points<br/>
        • Improved reuse potential: +{reuse_improvement:.1f} percentage points<br/><br/>
        
        These improvements demonstrate the significant environmental benefits of adopting 
        circular economy principles in metallurgy and mining operations."""
        
        return text
    
    def _create_comparison_chart(self, pathways: list) -> str:
        """Create comparison chart and return path to image file"""
        if not pathways:
            return None
        
        try:
            plt.figure(figsize=(10, 6))
            
            pathway_names = [p.get('name', '') for p in pathways]
            co2_values = [p.get('co2_equivalent', 0) for p in pathways]
            colors_list = ['#dc3545', '#28a745']  # Red for conventional, green for circular
            
            bars = plt.bar(pathway_names, co2_values, color=colors_list[:len(pathway_names)])
            plt.title('CO₂ Emissions Comparison', fontsize=16, fontweight='bold')
            plt.ylabel('CO₂ Equivalent (kg/kg metal)', fontsize=12)
            plt.xlabel('Pathway', fontsize=12)
            
            # Add value labels on bars
            for bar, value in zip(bars, co2_values):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(co2_values)*0.01,
                        f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            
            # Save to temporary file
            temp_dir = tempfile.gettempdir()
            chart_path = os.path.join(temp_dir, f"lca_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            print(f"Error creating chart: {e}")
            return None
    
    def _create_recommendations(self, data: Dict[str, Any]) -> str:
        """Create recommendations based on analysis results"""
        enhanced_data = data.get('enhanced_data', {})
        results = data.get('results', {})
        
        metal_type = enhanced_data.get('metalType', 'metal')
        production_route = enhanced_data.get('productionRoute', 'raw')
        
        recommendations = []
        
        # Production route recommendations
        if production_route == 'raw':
            recommendations.append(f"• Consider transitioning to recycled {metal_type} production to reduce environmental impact by up to 60-80%")
        
        # End-of-life recommendations
        eol = enhanced_data.get('endOfLife', '')
        if eol == 'landfill':
            recommendations.append("• Implement reuse or recycling programs instead of landfill disposal")
        elif eol == 'recycle':
            recommendations.append("• Explore direct reuse opportunities to further minimize environmental impact")
        
        # Energy efficiency recommendations
        energy_use = enhanced_data.get('energyUse', 0)
        if energy_use > 10:
            recommendations.append("• Investigate energy efficiency improvements and renewable energy sources")
        
        # Transport optimization
        transport = enhanced_data.get('transportDistance', 0)
        if transport > 500:
            recommendations.append("• Optimize supply chain logistics to reduce transport distances")
        
        # General circular economy recommendations
        recommendations.extend([
            f"• Develop partnerships with {metal_type} recyclers and reprocessors",
            "• Implement design for circularity principles in product development",
            "• Consider industrial symbiosis opportunities with other manufacturers"
        ])
        
        return "<br/>".join(recommendations)
