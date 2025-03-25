import streamlit as st
from trip_agent import TripCrew

st.title("✈️ AI Travel Planner")
st.markdown("Plan your dream trip with AI-powered suggestions!")

travel_type = st.selectbox("Select your travel type", ["Adventure", "Relaxation", "Cultural", "Romantic"])
interests = st.text_area("Enter your interests (e.g., beaches, museums, hiking, nightlife)", "museums, history")
season = st.selectbox("Preferred travel season", ["Winter", "Spring", "Summer", "Autumn"])
budget = st.number_input("Enter your budget (in USD)", min_value=500, max_value=10000, step=100, value=2000)

if st.button("Generate Travel Plan"):
    with st.spinner("Generating your travel plan..."):
        inputs = {
            "travel_type": travel_type,
            "interests": interests,
            "season": season,
            "budget": budget
        }
        trip_crew = TripCrew(inputs)
        crew = trip_crew.create_crew(selected_city="Paris", budget=budget)
        try:
            results = crew.kickoff()
        except Exception as e:
            st.error(f"Error running the crew: {str(e)}")
            results = [
                "- Paris: Great for culture. Rich in history and art.\n- Tokyo: Tech and tradition blend. Unique seasonal appeal.\n- Rome: Historical depth. Perfect for museum lovers.",
                "Paris: Visit Louvre, respect café etiquette, explore Montmartre hidden streets.",
                "Day 1: Arrive, visit Eiffel Tower (2h, metro). Day 2: Louvre (4h, walk). Day 3: Notre-Dame (2h, bus). Day 4: Montmartre (3h, metro). Day 5: Depart.",
                f"Paris Budget ({budget} USD): Hotel (800), Metro (50), Activities (600), Food (550)."
            ]

    st.subheader("🌍 Suggested Cities:")
    st.write(results[0])
    st.subheader("🏙️ City Insights:")
    st.write(results[1])
    st.subheader("📅 Travel Itinerary:")
    st.write(results[2])
    st.subheader("💰 Budget Plan:")
    st.write(results[3])