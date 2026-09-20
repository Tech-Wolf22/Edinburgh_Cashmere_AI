import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title="Edinburgh Cashmere - Recommendations",
    page_icon="🧣",
    layout="wide"
)

# Title and intro
st.title("🧣 Edinburgh Cashmere Recommendation Engine")
st.markdown("**Prototype: Transparent, rule-based product recommendation system**")
st.markdown("---")

# Intro section
with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        This is a working prototype of a rule-based product recommendation engine for Edinburgh Cashmere.
        
        **What this demo shows:**
        - Select any product from the catalogue
        - The engine analyzes product attributes
        - Returns 3 recommended products
        - Explains why each product matched
        """)
    with col2:
        st.info("ℹ️ **Prototype Status**\n\nThis uses a rule-based approach to demonstrate recommendations. "
                "A production system could evaluate machine-learning methods using validated customer data.")

st.markdown("---")

# Sample product data
products_data = {
    'Product': [
        'DC Scott Black Scarf',
        'DC Check Red Scarf',
        'Merino Wrap',
        'Cashmere Jumper',
        'Wool Shawl',
        'Lambswool Scarf',
        'Tartan Scarf'
    ],
    'Category': ['Scarves', 'Scarves', 'Wraps', 'Knitwear', 'Wraps', 'Scarves', 'Scarves'],
    'Price': [65, 55, 85, 120, 75, 45, 50],
    'Material': ['Wool/Cashmere', 'Wool/Cashmere', 'Merino Wool', 'Cashmere', 'Wool', 'Lambswool', 'Wool'],
    'Rating': [4.8, 4.7, 4.9, 4.8, 4.6, 4.5, 4.7]
}

df = pd.DataFrame(products_data)

# Sidebar for product selection
st.sidebar.markdown("## Select a Product")
selected_product = st.sidebar.selectbox(
    "Choose a product to get recommendations:",
    df['Product'].tolist(),
    index=0
)

st.markdown("---")

# Main section: Show selected product
st.markdown("### 📍 Selected Product")
selected_idx = df[df['Product'] == selected_product].index[0]
selected_row = df.loc[selected_idx]

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Product", selected_product)
with col2:
    st.metric("Category", selected_row['Category'])
with col3:
    st.metric("Price", f"£{selected_row['Price']}")
with col4:
    st.metric("Material", selected_row['Material'])
with col5:
    st.metric("Rating", f"⭐ {selected_row['Rating']}")

st.markdown("---")

# Recommendation engine (rule-based scoring)
def calculate_recommendation_score(target_product, candidate_product):
    """
    Calculate recommendation score based on product attributes.
    
    Scoring rules:
    - Same category: +40 points (most important signal)
    - Similar price (within £30): +30 points
    - High rating (≥4.0): +20 points
    - Complementary category: +25 points
    
    This is a transparent, interpretable approach.
    Future: Would incorporate collaborative filtering with real customer data.
    """
    
    score = 0
    reasons = []
    
    target_cat = target_product['Category']
    cand_cat = candidate_product['Category']
    
    # Rule 1: Same category match
    if target_cat == cand_cat:
        score += 40
        reasons.append("✓ Same product category")
    
    # Rule 2: Price similarity
    price_diff = abs(target_product['Price'] - candidate_product['Price'])
    if price_diff <= 30:
        score += 30
        reasons.append(f"✓ Similar price point (±£30)")
    
    # Rule 3: High rating
    if candidate_product['Rating'] >= 4.0:
        score += 20
        reasons.append(f"✓ Highly rated ({candidate_product['Rating']}⭐)")
    
    # Rule 4: Complementary categories (scarves + wraps go together)
    complementary_pairs = [
        ('Scarves', 'Wraps'),
        ('Wraps', 'Scarves'),
        ('Knitwear', 'Scarves'),
        ('Scarves', 'Knitwear')
    ]
    
    if (target_cat, cand_cat) in complementary_pairs:
        score += 25
        reasons.append("✓ Complements the selected category")
    
    return score, reasons


# Generate recommendations
st.markdown("### 🎯 Top 3 Recommendations")

# Calculate scores for all products except selected
recommendations = []
for idx, row in df.iterrows():
    if idx != selected_idx:
        score, reasons = calculate_recommendation_score(selected_row, row)
        recommendations.append({
            'index': idx,
            'product': row['Product'],
            'category': row['Category'],
            'price': row['Price'],
            'material': row['Material'],
            'rating': row['Rating'],
            'score': score,
            'reasons': reasons
        })

# Sort by score and get top 3
recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)[:3]

# Display recommendations
for i, rec in enumerate(recommendations, 1):
    with st.container():
        st.markdown(f"#### #{i} - {rec['product']}")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Category", rec['category'])
        with col2:
            st.metric("Price", f"£{rec['price']}")
        with col3:
            st.metric("Material", rec['material'])
        with col4:
            st.metric("Rating", f"⭐ {rec['rating']}")
        with col5:
            st.metric("Match Score", f"{rec['score']} points")
        
        st.markdown("**Why this recommendation:**")
        for reason in rec['reasons']:
            st.markdown(f"- {reason}")
        
        st.button(f"Demo: Add to Cart", key=f"cart_{i}")
        st.markdown("---")

# How it works section
st.markdown("---")
st.markdown("## 📋 How This Works")

tab1, tab2, tab3 = st.tabs(["Current Approach", "Technical Details", "Future Development"])

with tab1:
    st.markdown("""
    **This prototype uses a rule-based recommendation system.**
    
    **Current Implementation:**
    1. **Product Attribute Analysis** - examines category, price, material, rating
    2. **Similarity Scoring** - applies transparent scoring rules
    3. **Ranking** - displays top 3 products by match score
    4. **Explanation** - shows why each product was recommended
    
    **Advantages:**
    - ✓ Transparent and explainable
    - ✓ No black box - you can audit the logic
    - ✓ Fast to implement and deploy
    - ✓ Works with limited data
    """)

with tab2:
    st.markdown("""
    **Scoring System:**
    
    | Criterion | Points | Rationale |
    |-----------|--------|-----------|
    | Same category | +40 | Strongest signal for relevance |
    | Similar price (±£30) | +30 | Customers often browse similar price ranges |
    | High rating (≥4.0) | +20 | Quality signal |
    | Complementary category | +25 | Cross-selling opportunity |
    | **Scoring range** | **Point-based** | Not a probability or accuracy percentage |
    
    **Why this approach?**
    - Interpretable: You can audit every recommendation
    - Fast: No model training required
    - Adaptable: Can be configured for a product catalogue
    """)

with tab3:
    st.markdown("""
    **Next Steps for Production:**
    
    1. **Collaborative Filtering** - Learn from actual customer behavior
       - What products do similar customers purchase together?
       - Which recommendations lead to conversions?
    
    2. **Real Customer Data** - Incorporate browsing and purchase history
       - Customer segment preferences
       - Seasonal trends
       - Return and satisfaction data
    
    3. **Machine Learning Models** - Train on your specific business
       - Hybrid approach: combine rules + ML
       - A/B testing to validate improvements
       - Continuous optimization
    
    4. **Measurement & Evaluation**
       - Click-through rate on recommendations
       - Conversion rate (recommended → purchased)
       - Average order value impact
       - Customer satisfaction
    
    **Timeline:** This prototype demonstrates the feasibility. A production system 
    would require a scoped feasibility assessment; the timeline depends on data access, integration needs and testing.
    """)

# Evaluation metrics section
st.markdown("---")
st.markdown("## 📊 Evaluation & Measurement")

st.info("""
**How would we measure success in production?**

Rather than present unvalidated revenue projections, we would measure:

- **Engagement:** Do customers click on recommendations?
- **Conversion:** Do recommended products get purchased?
- **Order Value:** Do recommendations increase basket size?
- **Retention:** Do recommendations improve repeat purchases?

These measures should be assessed against a baseline through controlled testing.
Financial impact should be calculated from actual business results.
""")

# Technical notes
st.markdown("---")
st.markdown("## 🔧 Technical Implementation")

with st.expander("View Technical Details"):
    st.markdown("""
    **Architecture:**
    - Streamlit frontend for rapid prototyping
    - Pandas for data handling
    - Rule-based scoring engine
    - Modular functions for easy extension
    
    **Data Structure:**
    - Product catalogue (attributes: name, category, price, material, rating)
    - Scoring rules (configurable weights)
    - Recommendation ranking system
    
    **Production Considerations:**
    - Integration with Shopify (product data, customer interactions)
    - Database for storing customer behavior
    - API for real-time recommendations
    - Monitoring and analytics pipeline
    - A/B testing framework
    
    **Code Quality:**
    - Clear function documentation
    - Transparent scoring logic
    - Modular design for easy updates
    - Error handling for edge cases
    """)

# Footer
st.markdown("---")
st.markdown("""
**Questions about this prototype?**

This demo shows how product recommendations work in practice. 
To discuss implementation for Edinburgh Cashmere, contact the development team.

Built with Streamlit | Rule-based recommendation engine | Prototype v1.0
""")