import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

base_dir = "/Users/OFSy/Antigravity/proj_vct25/vct_stat/vct_2026"
images_dir = "/Users/OFSy/Antigravity/Porj_Port/images"

# Ensure directories exist
os.makedirs(images_dir, exist_ok=True)

# Set custom styling for dark mode/esports theme
plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = '#0a080e'
plt.rcParams['axes.facecolor'] = '#120f1a'
plt.rcParams['axes.edgecolor'] = '#2c253d'
plt.rcParams['grid.color'] = '#2c253d'
plt.rcParams['text.color'] = '#f3f3f5'
plt.rcParams['axes.labelcolor'] = '#a0a0ab'
plt.rcParams['xtick.color'] = '#a0a0ab'
plt.rcParams['ytick.color'] = '#a0a0ab'

print("Generating VCT 2026 analytics plots...")

# --- Plot 1: Agent Meta Pick Rates ---
agents_pr_file = os.path.join(base_dir, "agents/agents_pick_rates.csv")
if os.path.exists(agents_pr_file):
    df_agents_pr = pd.read_csv(agents_pr_file)
    df_agents_pr['Pick Rate Num'] = df_agents_pr['Pick Rate'].str.rstrip('%').astype(float)
    agent_pr_summary = df_agents_pr.groupby('Agent')['Pick Rate Num'].mean().reset_index()
    agent_pr_summary = agent_pr_summary.sort_values(by='Pick Rate Num', ascending=False).head(10)
    
    plt.figure(figsize=(10, 5.5))
    colors = ['#00f5d4' if a in ['waylay', 'tejo', 'vyse'] else '#9b5de5' for a in agent_pr_summary['Agent']]
    
    bars = plt.bar(agent_pr_summary['Agent'], agent_pr_summary['Pick Rate Num'], color=colors, edgecolor='#000', alpha=0.9, width=0.6)
    
    # Add values on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{yval:.1f}%", ha='center', va='bottom', color='#f3f3f5', fontsize=10)
        
    plt.title('VCT 2026 Top Agent Pick Rates (New Agents Highlighted in Cyan)', fontsize=14, fontweight='bold', pad=20, fontname='sans-serif', color='#00f5d4')
    plt.ylabel('Average Pick Rate (%)', fontsize=11)
    plt.ylim(0, 70)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'vct2026_agent_meta.png'), dpi=150, facecolor='#0a080e')
    plt.close()
    print("Agent Meta plot generated.")

# --- Plot 2: Pistol Win % vs Map Win % ---
scores_file = os.path.join(base_dir, "matches/scores.csv")
maps_scores_file = os.path.join(base_dir, "matches/maps_scores.csv")
eco_rounds_file = os.path.join(base_dir, "matches/eco_rounds.csv")

if os.path.exists(scores_file) and os.path.exists(maps_scores_file) and os.path.exists(eco_rounds_file):
    # Reconstruct team map win%
    df_maps_scores = pd.read_csv(maps_scores_file)
    team_map_stats = {}
    for idx, row in df_maps_scores.iterrows():
        tA, tB = row['Team A'], row['Team B']
        sA, sB = int(row['Team A Score']), int(row['Team B Score'])
        if tA not in team_map_stats: team_map_stats[tA] = {"played": 0, "won": 0}
        if tB not in team_map_stats: team_map_stats[tB] = {"played": 0, "won": 0}
        team_map_stats[tA]["played"] += 1
        team_map_stats[tB]["played"] += 1
        if sA > sB: team_map_stats[tA]["won"] += 1
        elif sB > sA: team_map_stats[tB]["won"] += 1
        
    df_eco = pd.read_csv(eco_rounds_file)
    df_pistols = df_eco[df_eco['Round Number'].isin([1, 13])]
    team_pistol_stats = {}
    for idx, row in df_pistols.iterrows():
        t = row['Team']
        outcome = row['Outcome']
        if t not in team_pistol_stats: team_pistol_stats[t] = {"played": 0, "won": 0}
        team_pistol_stats[t]["played"] += 1
        if outcome == "Win": team_pistol_stats[t]["won"] += 1
        
    # Combine
    plot_data = []
    for t in team_map_stats:
        if t in team_pistol_stats and team_map_stats[t]['played'] >= 10:
            map_win_pct = team_map_stats[t]['won'] / team_map_stats[t]['played'] * 100
            pistol_win_pct = team_pistol_stats[t]['won'] / team_pistol_stats[t]['played'] * 100
            plot_data.append({
                "Team": t,
                "Map Win %": map_win_pct,
                "Pistol Win %": pistol_win_pct
            })
    df_plot = pd.DataFrame(plot_data)
    
    plt.figure(figsize=(9, 6.5))
    sns.scatterplot(data=df_plot, x='Pistol Win %', y='Map Win %', s=200, color='#9b5de5', edgecolor='#00f5d4', linewidth=1.5, alpha=0.85)
    
    # Annotate top teams
    for idx, row in df_plot.iterrows():
        if row['Pistol Win %'] > 58 or row['Map Win %'] > 65 or row['Team'] in ['LEVIATÁN', 'Nongshim RedForce', 'Paper Rex']:
            plt.text(row['Pistol Win %'] + 0.8, row['Map Win %'] - 0.5, row['Team'], fontsize=9, color='#f3f3f5')
            
    # Trend line
    sns.regplot(data=df_plot, x='Pistol Win %', y='Map Win %', scatter=False, color='#ff007f', line_kws={"linestyle": "--", "alpha": 0.5})
    
    plt.title('Pistol Round Win % vs. Map Win % (Teams with 10+ Maps)', fontsize=14, fontweight='bold', pad=20, color='#00f5d4')
    plt.xlabel('Pistol Round Win %', fontsize=11)
    plt.ylabel('Map Win %', fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'vct2026_pistol_conversion.png'), dpi=150, facecolor='#0a080e')
    plt.close()
    print("Pistol Round Conversion plot generated.")

# --- Plot 3: Economy Win Rates ---
if os.path.exists(eco_rounds_file):
    eco_summary = df_eco.groupby(['Type', 'Outcome']).size().unstack(fill_value=0)
    eco_summary['Total'] = eco_summary['Win'] + eco_summary['Loss']
    eco_summary['Win Rate %'] = eco_summary['Win'] / eco_summary['Total'] * 100
    eco_summary = eco_summary.reset_index()
    
    # Sort from Eco to Full buy
    buy_order = {
        'Eco: 0-5k': 0,
        'Semi-buy: 10-20k': 1,
        'Force-buy: 5-10k': 2, # Note: check if there's any other categories
        'Full buy: 20k+': 3
    }
    eco_summary['Order'] = eco_summary['Type'].map(buy_order).fillna(4)
    eco_summary = eco_summary.sort_values(by='Order')
    
    plt.figure(figsize=(9, 5.5))
    bars = plt.bar(eco_summary['Type'], eco_summary['Win Rate %'], color=['#ff007f', '#ff7b54', '#9b5de5', '#00f5d4'], edgecolor='#000', alpha=0.85, width=0.55)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{yval:.2f}%", ha='center', va='bottom', color='#f3f3f5', fontweight='bold')
        
    plt.title('Round Win Rate by Loadout Buy Type', fontsize=14, fontweight='bold', pad=20, color='#00f5d4')
    plt.ylabel('Win Rate (%)', fontsize=11)
    plt.ylim(0, 70)
    plt.grid(axis='y', linestyle='--', alpha=0.2)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'vct2026_economy_efficiency.png'), dpi=150, facecolor='#0a080e')
    plt.close()
    print("Economy Efficiency plot generated.")

# --- Plot 4: Nongshim RedForce Performance Stats ---
players_file = os.path.join(base_dir, "players_stats/players_stats.csv")
if os.path.exists(players_file):
    df_p = pd.read_csv(players_file)
    df_p['Rating'] = pd.to_numeric(df_p['Rating'], errors='coerce')
    df_p['Average Combat Score'] = pd.to_numeric(df_p['Average Combat Score'], errors='coerce')
    
    ns_roster = df_p[df_p['Teams'] == 'Nongshim RedForce'].groupby('Player')[['Rating', 'Average Combat Score']].mean().reset_index()
    ns_roster = ns_roster.sort_values(by='Rating', ascending=False)
    
    plt.figure(figsize=(9, 5.5))
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    
    x = range(len(ns_roster))
    bars = ax1.bar(ns_roster['Player'], ns_roster['Rating'], color='#00f5d4', alpha=0.7, width=0.4, label='Avg. Rating')
    line = ax2.plot(ns_roster['Player'], ns_roster['Average Combat Score'], color='#ff007f', marker='o', linewidth=2.5, markersize=8, label='Avg. ACS')
    
    # labels and legends
    ax1.set_ylabel('Average Rating', color='#00f5d4', fontsize=11)
    ax2.set_ylabel('Average Combat Score (ACS)', color='#ff007f', fontsize=11)
    ax1.set_ylim(0, 1.8)
    ax2.set_ylim(0, 320)
    ax1.tick_params(axis='y', labelcolor='#00f5d4')
    ax2.tick_params(axis='y', labelcolor='#ff007f')
    
    # Title
    plt.title('Nongshim RedForce 2026 Player Roster Stats Overview', fontsize=14, fontweight='bold', pad=20, color='#00f5d4')
    ax1.grid(axis='y', linestyle='--', alpha=0.2)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'vct2026_nongshim_performance.png'), dpi=150, facecolor='#0a080e')
    plt.close()
    print("Nongshim Performance plot generated.")

print("All VCT 2026 charts successfully saved in Porj_Port/images/!")
