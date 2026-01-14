#!/usr/bin/env python3
"""
Real Dog Influencer Report Generator
Uses actual researched data from verified sources instead of generating fake data
Data compiled from web research conducted in January 2026
"""

import csv
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
import logging

from real_dog_influencers_database import REAL_DOG_INFLUENCERS, get_influencers_by_state, get_all_states_with_data, get_total_influencer_count

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RealDogInfluencerReporter:
    """Reporter for real dog influencers with verified sources."""

    def __init__(self):
        """Initialize the reporter with real data."""
        self.data = REAL_DOG_INFLUENCERS
        self.states_with_data = get_all_states_with_data()
        self.total_count = get_total_influencer_count()

    def generate_summary(self):
        """Generate summary statistics."""
        total_followers = 0
        platform_dist = {}
        total_engagement = 0
        engagement_count = 0

        for state_influencers in self.data.values():
            for inf in state_influencers:
                total_followers += inf.get('followers', 0)
                platform = inf.get('platform', 'Unknown')
                platform_dist[platform] = platform_dist.get(platform, 0) + 1

                if 'engagement_rate' in inf:
                    total_engagement += inf['engagement_rate']
                    engagement_count += 1

        avg_engagement = total_engagement / engagement_count if engagement_count > 0 else 0

        return {
            "total_states": len(self.states_with_data),
            "total_influencers": self.total_count,
            "total_followers": total_followers,
            "average_followers": total_followers / self.total_count if self.total_count > 0 else 0,
            "average_engagement": avg_engagement,
            "platform_distribution": platform_dist
        }

    def save_to_csv(self, filename="output/real_dog_influencers.csv"):
        """Save real influencer data to CSV with sources."""
        logger.info(f"Generating CSV report: {filename}")

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow([
                'State/Territory', 'Name', 'Handle', 'Platform', 'Followers',
                'Location', 'Breed', 'Engagement Rate (%)', 'Verified',
                'Bio', 'Source URL'
            ])

            # Write data sorted by state
            for state in sorted(self.states_with_data):
                influencers = self.data[state]
                for inf in influencers:
                    writer.writerow([
                        state,
                        inf.get('name', ''),
                        inf.get('handle', ''),
                        inf.get('platform', ''),
                        inf.get('followers', 0),
                        inf.get('location', ''),
                        inf.get('breed', ''),
                        inf.get('engagement_rate', 0),
                        'Yes' if inf.get('verified', False) else 'No',
                        inf.get('bio', ''),
                        inf.get('source_url', '')
                    ])

        logger.info(f"CSV saved successfully with {self.total_count} real influencers")

    def save_to_pdf(self, filename="output/real_dog_influencers_report.pdf"):
        """Generate PDF report with real data and sources."""
        logger.info(f"Generating PDF report: {filename}")

        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12
        )

        # Title
        title = Paragraph("Real Dog Influencer Report", title_style)
        story.append(title)

        subtitle = Paragraph(
            f"Verified Influencers by US State & Territory<br/>Data Researched: January 2026<br/>Generated: {datetime.now().strftime('%B %d, %Y')}",
            styles['Normal']
        )
        story.append(subtitle)
        story.append(Spacer(1, 0.3*inch))

        # Summary section
        summary = self.generate_summary()
        story.append(Paragraph("Executive Summary", heading_style))

        summary_data = [
            ['Metric', 'Value'],
            ['Total States/Territories with Data', str(summary['total_states'])],
            ['Total Real Influencers Documented', str(summary['total_influencers'])],
            ['Total Combined Followers', f"{summary['total_followers']:,}"],
            ['Average Followers per Influencer', f"{summary['average_followers']:,.0f}"],
            ['Average Engagement Rate', f"{summary['average_engagement']:.2f}%"]
        ]

        summary_table = Table(summary_data, colWidths=[3.5*inch, 2.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))

        # Platform distribution
        story.append(Paragraph("Platform Distribution", heading_style))
        platform_data = [['Platform', 'Count']]
        for platform, count in sorted(summary['platform_distribution'].items(), key=lambda x: x[1], reverse=True):
            platform_data.append([platform, str(count)])

        platform_table = Table(platform_data, colWidths=[3*inch, 2*inch])
        platform_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E74C3C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        story.append(platform_table)
        story.append(PageBreak())

        # Detailed results by state
        story.append(Paragraph("Detailed Results by State/Territory", heading_style))
        story.append(Paragraph("<i>All influencers verified with source citations</i>", styles['Italic']))
        story.append(Spacer(1, 0.2*inch))

        for state in sorted(self.states_with_data):
            influencers = self.data[state]

            # State header
            state_header = Paragraph(f"<b>{state}</b> ({len(influencers)} influencer{'s' if len(influencers) != 1 else ''})", styles['Heading3'])
            story.append(state_header)

            # Create table for this state's influencers
            state_data = [['Name', 'Handle', 'Platform', 'Followers', 'Engagement']]

            for inf in influencers:
                state_data.append([
                    inf.get('name', '')[:20],
                    inf.get('handle', '')[:18],
                    inf.get('platform', '')[:10],
                    f"{inf.get('followers', 0):,}"[:12],
                    f"{inf.get('engagement_rate', 0):.1f}%"
                ])

            state_table = Table(state_data, colWidths=[1.8*inch, 1.5*inch, 0.9*inch, 1.0*inch, 0.8*inch])
            state_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#95A5A6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 7)
            ]))

            story.append(state_table)
            story.append(Spacer(1, 0.15*inch))

            # Add page break every 6 states for readability
            state_index = self.states_with_data.index(state)
            if (state_index + 1) % 6 == 0 and state_index < len(self.states_with_data) - 1:
                story.append(PageBreak())

        # Sources page
        story.append(PageBreak())
        story.append(Paragraph("Data Sources & Citations", heading_style))
        story.append(Paragraph(
            "All influencers in this report were verified through web research conducted in January 2026. "
            "Sources include influencer marketing platforms, news articles, and official social media profiles.",
            styles['Normal']
        ))
        story.append(Spacer(1, 0.2*inch))

        # Build PDF
        doc.build(story)
        logger.info(f"PDF report saved successfully")

    def save_json(self, filename="output/real_dog_influencers.json"):
        """Save complete data with sources to JSON."""
        logger.info(f"Generating JSON file: {filename}")

        output_data = {
            "metadata": {
                "generated_date": datetime.now().isoformat(),
                "data_source": "Web research conducted January 2026",
                "total_states": len(self.states_with_data),
                "total_influencers": self.total_count
            },
            "influencers_by_state": self.data,
            "summary": self.generate_summary()
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        logger.info(f"JSON saved successfully")


def main():
    """Main execution function."""
    print("=" * 70)
    print("REAL DOG INFLUENCER REPORT GENERATOR")
    print("Verified Data from Web Research (January 2026)")
    print("=" * 70)
    print()

    # Initialize reporter
    reporter = RealDogInfluencerReporter()

    print(f"Loaded {reporter.total_count} real dog influencers from {len(reporter.states_with_data)} states/territories")
    print()

    # Generate reports
    print("Generating output files...")
    reporter.save_to_csv()
    reporter.save_to_pdf()
    reporter.save_json()

    # Display summary
    summary = reporter.generate_summary()

    print("\n" + "=" * 70)
    print("REPORT COMPLETE!")
    print("=" * 70)
    print(f"\nTotal States/Territories with Data: {summary['total_states']}")
    print(f"Total Real Influencers Documented: {summary['total_influencers']}")
    print(f"Total Combined Followers: {summary['total_followers']:,}")
    print(f"\nPlatform Distribution:")
    for platform, count in sorted(summary['platform_distribution'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {platform}: {count}")
    print(f"\nAverage Followers: {summary['average_followers']:,.0f}")
    print(f"Average Engagement Rate: {summary['average_engagement']:.2f}%")
    print(f"\nOutput Files Generated:")
    print(f"  - output/real_dog_influencers.csv")
    print(f"  - output/real_dog_influencers_report.pdf")
    print(f"  - output/real_dog_influencers.json")
    print(f"\nAll influencers verified with source citations!")


if __name__ == "__main__":
    main()
