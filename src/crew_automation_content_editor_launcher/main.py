#!/usr/bin/env python
import sys
import os
from crew_automation_content_editor_launcher.crew import CrewAutomationContentEditorLauncherCrew
from crew_automation_content_editor_launcher.utils.logger import logger

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding unnecessary logic into this file.

def run():
    """
    Run the crew with Siebert Financial inputs.
    """
    # Get content request from user input
    content_request = input("Enter your content request: ")
    
    inputs = {
        'brand_name': 'Siebert Financial',
        'tone_of_voice': 'Professional, trustworthy, and approachable',
        'primary_target': 'Individual investors looking for reliable financial services',
        'content_request': content_request,
        'brand_info_csv': os.path.join(os.getcwd(), 'RAG', 'Rag 1', 'brand_info.csv'),
        'best_practices_csv': os.path.join(os.getcwd(), 'RAG', 'Rag 2', 'best_practices.csv'),
        'compliance_info_csv': os.path.join(os.getcwd(), 'RAG', 'Rag 3', 'compliance_info.csv - Foglio1.csv'),
        'secondary_target': 'Financial advisors and wealth management professionals',
        'unique_selling_points': 'Over 50 years of experience, personalized service, competitive fees',
        'brand_colors': 'Blue and white',
        'keywords': 'investment advisory, wealth management, financial planning, retirement planning',
        'avoid_terms': 'guaranteed returns, risk-free, get rich quick',
        'structure': 'Introduction, Benefits, Services Overview, Client Testimonials, Call to Action',
        'ideal_length': '800-1200 words',
        'required_elements': 'Company history, service descriptions, contact information',
        'mandatory_elements': 'Regulatory disclosures, fee transparency',
        'forbidden_elements': 'Specific return promises, competitor criticism',
        'disclaimers': 'Investment advisory services involve risk. Past performance is not indicative of future results.'
    }
    
    logger.log_info("Starting Content Editor Crew with Siebert Financial inputs")
    result = CrewAutomationContentEditorLauncherCrew().crew().kickoff(inputs=inputs)
    logger.log_info("Content Editor Crew execution completed")
    return result


def train():
    """Train the crew for a given number of iterations."""
    inputs = {
        'brand_name': 'Siebert Financial',
        'tone_of_voice': 'Professional, trustworthy, and approachable',
        'primary_target': 'Individual investors looking for reliable financial services',
        'content_request': 'Create a blog post about the benefits of Siebert Financial\'s investment advisory services',
        'brand_info_csv': os.path.join(os.getcwd(), 'RAG', 'Rag 1', 'brand_info.csv'),
        'best_practices_csv': os.path.join(os.getcwd(), 'RAG', 'Rag 2', 'best_practices.csv'),
        'compliance_info_csv': os.path.join(os.getcwd(), 'RAG', 'Rag 3', 'compliance_info.csv - Foglio1.csv'),
        'secondary_target': 'Financial advisors and wealth management professionals',
        'unique_selling_points': 'Over 50 years of experience, personalized service, competitive fees',
        'brand_colors': 'Blue and white',
        'keywords': 'investment advisory, wealth management, financial planning, retirement planning',
        'avoid_terms': 'guaranteed returns, risk-free, get rich quick',
        'structure': 'Introduction, Benefits, Services Overview, Client Testimonials, Call to Action',
        'ideal_length': '800-1200 words',
        'required_elements': 'Company history, service descriptions, contact information',
        'mandatory_elements': 'Regulatory disclosures, fee transparency',
        'forbidden_elements': 'Specific return promises, competitor criticism',
        'disclaimers': 'Investment advisory services involve risk. Past performance is not indicative of future results.'
    }
    try:
        logger.log_info(f"Training Content Editor Crew for {sys.argv[1]} iterations")
        CrewAutomationContentEditorLauncherCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
        logger.log_info("Training completed successfully")
    except Exception as e:
        logger.log_error(f"An error occurred while training the crew: {str(e)}")
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        logger.log_info(f"Replaying Content Editor Crew from task {sys.argv[1]}")
        CrewAutomationContentEditorLauncherCrew().crew().replay(task_id=sys.argv[1])
        logger.log_info("Replay completed successfully")
    except Exception as e:
        logger.log_error(f"An error occurred while replaying the crew: {str(e)}")
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'brand_name': 'Siebert Financial',
        'tone_of_voice': 'Professional, informative, and educational',
        'primary_target': 'Individual investors interested in diversifying their portfolios',
        'content_request': 'Create a comprehensive guide about mutual funds offered by Siebert Financial, explaining their benefits, types, and how to get started',
        'brand_info_csv': os.path.join(os.getcwd(), 'RAG', 'Rag 1', 'brand_info.csv'),
        'best_practices_csv': os.path.join(os.getcwd(), 'RAG', 'Rag 2', 'best_practices.csv'),
        'compliance_info_csv': os.path.join(os.getcwd(), 'RAG', 'Rag 3', 'compliance_info.csv - Foglio1.csv'),
        'secondary_target': 'Financial advisors looking to recommend mutual fund options to clients',
        'unique_selling_points': 'Wide range of fund options, low expense ratios, experienced fund managers',
        'brand_colors': 'Blue and white',
        'keywords': 'mutual funds, portfolio diversification, fund management, investment strategy, retirement planning, asset allocation',
        'avoid_terms': 'guaranteed returns, risk-free investments, market timing, hot stock tips',
        'structure': 'Introduction, Types of Mutual Funds, Benefits of Investing, How to Choose the Right Fund, Getting Started with Siebert, Conclusion',
        'ideal_length': '1000-1500 words',
        'required_elements': 'Fund performance metrics, expense ratio explanations, investment minimums, Siebert\'s fund selection process',
        'mandatory_elements': 'Risk disclosures, fee transparency, diversification importance',
        'forbidden_elements': 'Specific return promises, competitor criticism, tax advice',
        'disclaimers': 'Mutual fund investments are subject to market risks. Past performance is not indicative of future results. Please read the prospectus carefully before investing.'
    }
    try:
        logger.log_info("Testing Content Editor Crew")
        result = CrewAutomationContentEditorLauncherCrew().crew().test(inputs=inputs, n_iterations=5, eval_llm='gpt-4')
        logger.log_info("Test completed successfully")
        return result
    except Exception as e:
        logger.log_error(f"An error occurred while testing the crew: {str(e)}")
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "train" and len(sys.argv) > 3:
            train()
        elif sys.argv[1] == "replay" and len(sys.argv) > 2:
            replay()
        elif sys.argv[1] == "test":
            test()
        else:
            print("Invalid command. Use 'train', 'replay', or 'test'.")
    else:
        run()
