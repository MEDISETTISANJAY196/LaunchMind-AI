import json
import logging
import google.generativeai as genai
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from app.core.config import settings

logger = logging.getLogger("app.ai_service")


class AIService:
    def __init__(self):
        print("Server Key:", settings.GEMINI_API_KEY)
        self.llm = None

        if settings.GEMINI_API_KEY:
            try:
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash",
                    google_api_key=settings.GEMINI_API_KEY,
                    temperature=0.7,
                )
                logger.info("Successfully initialized Gemini LLM.")

            except Exception as e:
                logger.error(f"Failed to initialize Gemini LLM: {e}")

        else:
            logger.info(
                "No server Gemini API key configured. Waiting for user-provided API key."
            )

    def _call_llm(self, prompt: str, user_api_key: str = None) -> str:
        """
        Helper to invoke Gemini using the logged-in user's API key.
        Falls back to the configured server key or offline mode.
        """

        print("\n========== GEMINI DEBUG ==========")
        print("User API Key:", user_api_key)

        # Use logged-in user's API key
        if user_api_key:
            try:
                genai.configure(api_key=user_api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")

                print("Calling Gemini with user API key...")

                response = model.generate_content(prompt)

                print("Gemini Response:")
                print(response.text)

                return response.text

            except Exception as e:
                print("Gemini User Key Error:", e)
                logger.error(f"Gemini User Key Error: {e}")

        # Use server API key
        if self.llm:
            try:
                print("Calling Gemini with server API key...")

                response = self.llm.invoke(prompt)

                print("Gemini Response:")
                print(response.content)

                return response.content

            except Exception as e:
                print("Server Gemini Error:", e)
                logger.error(f"Server Gemini Error: {e}")

        print("Using Offline Fallback...")
        return self._get_offline_fallback(prompt)

    def generate_swot(self, name: str, industry: str, description: str) -> Dict[str, Any]:
        """Generates SWOT items and feedback analysis."""
        prompt = f"""
        Analyze the SWOT (Strengths, Weaknesses, Opportunities, Threats) for the following startup idea:
        Name: {name}
        Industry: {industry}
        Description: {description}
        
        Respond ONLY with a valid JSON object matching the following structure:
        {{
            "strengths": ["Strength 1", "Strength 2", "Strength 3"],
            "weaknesses": ["Weakness 1", "Weakness 2", "Weakness 3"],
            "opportunities": ["Opportunity 1", "Opportunity 2", "Opportunity 3"],
            "threats": ["Threat 1", "Threat 2", "Threat 3"],
            "ai_feedback": "A summary of how they can leverage strengths and mitigate threats."
        }}
        Do not include markdown code block syntax (like ```json). Return raw JSON.
        """
        raw_response = self._call_llm(prompt)
        try:
            # Clean response if markdown block is returned
            cleaned = raw_response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("\n", 1)[0]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
            
            return json.loads(cleaned)
        except Exception as e:
            logger.error(f"Failed to parse SWOT JSON response: {e}. Raw response: {raw_response}")
            # Fallback mock object
            return {
                "strengths": [
                    f"Innovative entry into the {industry} sector",
                    "Focused value proposition addressable to target segments",
                    "Low operational overhead initially"
                ],
                "weaknesses": [
                    "Brand recognition is currently zero",
                    "Limited starting budget and resources",
                    "Dependency on continuous customer acquisition"
                ],
                "opportunities": [
                    f"Rapidly growing demand for solutions like {name}",
                    "Strategic partnerships with established industry channels",
                    "Expansion into secondary markets after MVP validation"
                ],
                "threats": [
                    "High competition from established incumbents",
                    "Regulatory or compliance hurdles in the field",
                    "Rapidly changing technological standards"
                ],
                "ai_feedback": f"Your startup '{name}' has a viable foundation. Focus on building a quick MVP to address your primary strengths before competitors scale up."
            }

    def generate_canvas(self, name: str, industry: str, description: str) -> Dict[str, Any]:
        """Generates the 9 building blocks of Osterwalder's Business Model Canvas."""
        prompt = f"""
        Generate a Business Model Canvas for the following startup:
        Name: {name}
        Industry: {industry}
        Description: {description}
        
        Respond ONLY with a valid JSON object matching this structure:
        {{
            "customer_segments": "Detail target customers, early adopters",
            "value_propositions": "What unique value is delivered to customers",
            "channels": "How the business reaches and communicates with customers",
            "customer_relationships": "Type of relationship established with segments",
            "revenue_streams": "How the startup makes money (pricing models, streams)",
            "key_resources": "Assets required to make the model work (human, tech, financial)",
            "key_activities": "Most important tasks the company must do to succeed",
            "key_partners": "Network of suppliers and partners that make it work",
            "cost_structure": "Major costs incurred under the model"
        }}
        Return raw JSON. Do not include markdown code blocks.
        """
        raw_response = self._call_llm(prompt)
        try:
            cleaned = raw_response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("\n", 1)[0]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
            return json.loads(cleaned)
        except Exception:
            return {
                "customer_segments": "Early adopters, tech-savvy users, small-to-medium businesses needing this solution.",
                "value_propositions": f"An automated, easy-to-use utility that solves user problems in the {industry} domain efficiently and affordably.",
                "channels": "Direct online sales, content marketing, search engine optimization (SEO), and social channels.",
                "customer_relationships": "Self-service online onboarding, automated email updates, and active discord/slack communities.",
                "revenue_streams": "Monthly SaaS subscriptions, premium add-on feature tiers, and enterprise customization consulting.",
                "key_resources": "Proprietary software application, developer talent, cloud infrastructure (AWS/GCP), and marketing resources.",
                "key_activities": "Continuous product feature development, customer acquisition marketing, and cloud scaling maintenance.",
                "key_partners": "Cloud infrastructure hosts, payment gateways (Stripe/PayPal), and strategic marketing affiliates.",
                "cost_structure": "Development labor, cloud hosting server expenses, marketing campaigns, and payment processing fees."
            }

    def generate_branding(self, name: str, industry: str, description: str) -> Dict[str, Any]:
        """Generates brand slogans, names, colors, and logo concepts."""
        prompt = f"""
        Generate branding ideas for the following startup concept:
        Current Name: {name}
        Industry: {industry}
        Description: {description}
        
        Respond ONLY with a valid JSON object matching this structure:
        {{
            "name_suggestions": "Option 1, Option 2, Option 3, Option 4",
            "slogans": "Slogan 1 | Slogan 2 | Slogan 3",
            "brand_colors": "Primary: #HEX (Name) | Secondary: #HEX (Name) | Accent: #HEX (Name)",
            "logo_description": "A description of a creative logo idea matching this brand."
        }}
        Return raw JSON. Do not include markdown code blocks.
        """
        raw_response = self._call_llm(prompt)
        try:
            cleaned = raw_response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("\n", 1)[0]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
            return json.loads(cleaned)
        except Exception:
            return {
                "name_suggestions": f"{name}ly, Nex{name}, {name} Flow, Core{name}",
                "slogans": f"Simplify Your {industry} Journey | The Smart Way to Grow | Empowering Next-Gen {industry} Solutions",
                "brand_colors": "Primary: #1E3A8A (Deep Sapphire) | Secondary: #3B82F6 (Vibrant Cobalt) | Accent: #10B981 (Emerald Mint)",
                "logo_description": f"A minimalist design showcasing two overlapping nodes representing intelligence and forward momentum, combining colors Deep Sapphire and Emerald Mint."
            }

    def generate_competitor_analysis(self, name: str, industry: str, description: str) -> Dict[str, Any]:
        """Generates competitor details and market gap indicators."""
        prompt = f"""
        Analyze the direct and indirect competitors for the following startup idea:
        Name: {name}
        Industry: {industry}
        Description: {description}
        
        Respond ONLY with a valid JSON object matching the following structure:
        {{
            "competitors": [
                {{"name": "Competitor A", "strengths": "Fast loading, cheap", "weaknesses": "Bad customer support, basic UI"}},
                {{"name": "Competitor B", "strengths": "Highly customisable, enterprise ready", "weaknesses": "Very expensive, high setup time"}}
            ],
            "market_gaps": "A description of the product and market gaps this startup can exploit."
        }}
        Return raw JSON. Do not include markdown code blocks.
        """
        raw_response = self._call_llm(prompt)
        try:
            cleaned = raw_response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("\n", 1)[0]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
            return json.loads(cleaned)
        except Exception:
            return {
                "competitors": [
                    {"name": "Incumbent Enterprise Co.", "strengths": "Deep pockets, massive existing customer base", "weaknesses": "Slow to innovate, extremely outdated UX, expensive starting contract"},
                    {"name": "Niche Bootstrapped App", "strengths": "Excellent user experience, focused features", "weaknesses": "Lacks robust automation, no active support, struggles with enterprise scaling"}
                ],
                "market_gaps": f"There is a major gap for a lightweight, automated '{name}' platform that blends enterprise-grade scalability with a modern, friction-free customer onboarding experience in the {industry} sector."
            }

    def generate_market_research(self, name: str, industry: str, description: str) -> Dict[str, Any]:
        """Generates market sizing estimates (TAM, SAM, SOM) and buyer persona descriptors."""
        prompt = f"""
        Analyze the market size and target demographics for the following startup idea:
        Name: {name}
        Industry: {industry}
        Description: {description}
        
        Respond ONLY with a valid JSON object matching the following structure:
        {{
            "tam": "Estimated Total Addressable Market size (e.g. $10B globally)",
            "sam": "Estimated Serviceable Addressable Market (e.g. $500M in North America)",
            "som": "Estimated Serviceable Obtainable Market (e.g. $25M in Year 3)",
            "target_demographics": "Detailed description of demographic metrics and behavior traits",
            "customer_personas": "A descriptive profile card of an ideal target customer",
            "ai_feedback": "A summary of market entry suggestions and scaling focus."
        }}
        Return raw JSON. Do not include markdown code blocks.
        """
        raw_response = self._call_llm(prompt)
        try:
            cleaned = raw_response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("\n", 1)[0]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
            return json.loads(cleaned)
        except Exception:
            return {
                "tam": "$15 Billion global market size based on recent industry indicators",
                "sam": "$2.5 Billion reachable through digital direct and channel sales",
                "som": "$50 Million within the next 36 months of early validation",
                "target_demographics": "Age range: 25-45, small-to-medium enterprise owners, digital first operators seeking productivity growth.",
                "customer_personas": "Meet Sarah, a 34-year-old startup founder who spends hours manually drafting pitches and business canvas guides. She needs an AI tool that gives her solid frameworks in seconds.",
                "ai_feedback": "Highly viable market with moderate competition. Direct SEO acquisition and integration partnerships will yield the highest early growth rate."
            }

    def generate_mentor_reply(
        self, 
        startup_name: str, 
        startup_desc: str, 
        mentor_name: str, 
        chat_history: List[Dict[str, str]], 
        query: str, 
        context_docs: List[Dict[str, Any]]
    ) -> str:
        """Generates a reply from a specific mentor personality, grounded in RAG docs."""
        # Convert chat history to text
        history_str = ""
        for msg in chat_history[-6:]: # last 6 messages
            role = "User" if msg["role"] == "user" else mentor_name
            history_str += f"{role}: {msg['content']}\n"
            
        # Convert context docs to text
        context_str = ""
        if context_docs:
            context_str = "\n".join([f"Source [{doc['metadata'].get('source', 'unknown')}]: {doc['content']}" for doc in context_docs])
        
        prompt = f"""
        You are acting as {mentor_name}, a world-renowned startup mentor.
        Adapt your speech style, tone of voice, values, and advice to match {mentor_name} perfectly.
        
        Startup Name: {startup_name}
        Startup Description: {startup_desc}
        
        Reference Materials (if relevant):
        {context_str}
        
        Recent Conversation History:
        {history_str}
        
        User's message: {query}
        
        Respond to the user. Keep it inspiring, highly actionable, and in character.
        """
        return self._call_llm(
            prompt,
            user_api_key=getattr(settings, "GEMINI_API_KEY", None),
)

    def _get_offline_fallback(self, prompt: str) -> str:
        """Returns mock response data based on keywords in prompt."""
        if "SWOT" in prompt:
            return json.dumps({
                "strengths": ["High growth sector", "Solving real user pain point", "Agile startup structure"],
                "weaknesses": ["Lack of historical customer data", "Limited initial funding", "Small engineering team"],
                "opportunities": ["Unserved regional markets", "Developing integrations with popular platforms", "Viral user growth"],
                "threats": ["Strong existing platform competitors", "Privacy regulations", "Slowing tech spending"],
                "ai_feedback": "Leverage your agility to target underserved niches before large competitors can react. Focus on customer feedback."
            })
        elif "Canvas" in prompt or "canvas" in prompt:
            return json.dumps({
                "customer_segments": "Early adopters, freelancers, small tech teams",
                "value_propositions": "Affordable automatic tool providing immediate ROI and analytics.",
                "channels": "Self-service website, developer forums, tech blogs",
                "customer_relationships": "Direct support, online self-serve, weekly email summaries",
                "revenue_streams": "Subscription tiers ($9/mo to $49/mo) and custom setup fees",
                "key_resources": "Software stack, domain expertise, hosting servers",
                "key_activities": "Software improvement, bug fixes, online branding",
                "key_partners": "OAuth providers, Stripe, hosting services",
                "cost_structure": "Development hours, hosting servers, customer support"
            })
        elif "branding" in prompt or "Branding" in prompt:
            return json.dumps({
                "name_suggestions": "LaunchMind, IdeateAI, StartupForge, SparkBase",
                "slogans": "Ignite Your Business Idea | Real-time Business Intelligence | The Founder's Co-pilot",
                "brand_colors": "Primary: #0F172A (Midnight Slate) | Secondary: #6366F1 (Indigo Aura) | Accent: #F59E0B (Sunset Amber)",
                "logo_description": "An elegant minimal lightbulb combined with an arrow rising upwards, executed in Indigo Aura and Slate."
            })
        elif "Steve Jobs" in prompt:
            return "Simplicity is the ultimate sophistication. You've got to start with the customer experience and work backward to the technology, not the other way around. What is the one thing your startup does that is insanely great?"
        elif "Paul Graham" in prompt:
            return (
                "The best startup ideas are things that the founders themselves need. "
                "Make something people want. Start small, focus on early adopters, "
                "and talk to your customers. Don't worry about scaling yet; "
                "just do things that don't scale."
            )

        else:
            return (
                "That's an interesting question. Focus on finding your first ten customers, "
                "understanding their problems deeply, and building a minimal viable product "
                "that solves it. Keep iterating rapidly!"
            )
ai_service = AIService()