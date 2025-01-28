---
title: Writing a Stellaris Mod
summary: The process of getting my mod, Gender Diversity & Politics, to release. Game design in a "why would I touch that" space, handling sensitive topics in game design and my careful considerations thereto, and getting sidetracked with parsing.
date: 2025-01-27
tags: gamedev,architecture
toc: true
---

## Introduction
Stellaris is a science fiction story simulator developed by Paradox Studios and published by its parent company, Paradox Interactive. Technically, the niche it occupies is grand strategy with elements of the 4X genre, the “explore, expand, exploit, exterminate” that the Civilization series made famous, but I think that description does it a disservice. It’s more similar to Dwarf Fortress or EVE online where a story emerges out of the latent space created by the game’s mechanics and player(s)‘s imagination and ingenuity, even more so than its sister games, Crusader Kings, Hearts of Iron, et al.

The player becomes the “soul of the nation” of a fledgling interstellar empire taking their first steps outside of their home star system. This soular role is like playing as a collective unconsciousness of a nation, a ghost in the machine directing your nation’s whims; you, the player, select your expansion targets, you react to emergent or scripted events, you conduct diplomacy with aliens states, but it never feels like you’re fully in control.

The individuals (or “pops”) and leaders in your nation have thoughts and beliefs of their own -- represented by game mechanics like happiness and faction support -- that are influenced by the actions you take as the nation. Different government types present this concept in different ways; a hive-minded rogue AI will give you more direct control over the citizenry, while a Star Trek-like direct democracy makes individual citizens more powerful. Regardless of government or species or other factors, the player’s influence remains the dominant force.

Recently, I played a game as a direct democracy of humans, who had been given FTL and other future technology by an alien corporation. That allowed the new “Sol Foundation” to begin spreading to the stars, curing cancer, defeating aging -- the works. But, my humans owed a massive debt to the corporation, tanking our economy and spurring xenophobia. There was no reason for the terms of our agreement to be so outrageous. These aliens were simply taking advantage of a nascent interstellar nation.

As the Sol Foundation embarked to the stars, they were aggressive and antagonistic toward other alien civilizations. Their first encounter had been so negative, why shouldn’t the others? But their galactic neighbours were peaceable and kind. There were other threats to deal with than some rowdy humans, who weren’t the worst thing in the south-west quadrant of the galaxy by a mile. They routinely extended trade offers and defensive pacts, which by realpolitik the Sol Foundation would be foolish to not accept and slowly, so slowly, they began to unwind the decades, centuries, of anti-alien attitude. It came to a head when another nation affected by the corporation reached out with something unheard of: a migration treaty, allowing for free movement between their nations. The human’s core xenophobia was coming undone.

This is one of my favourite parts of Stellaris, the internal affairs of your nation outside of economics. It is sadly an underutilized and under-explored aspect in the base game and its expansions (which I’ll call “vanilla” from now on). There are very few instances of internal politics affecting your empire. But this playthrough made me think of what other pieces of internal politics could be improved on from vanilla.

One particular aspect that is lacking but has *some* support is gender politics. Historically, resource access, inheritance laws, cultural narratives, and many other cultural aspects have been key drivers of gendered power dynamics, shaping societal structures in profound ways. This provides a useful lens for examining how power might manifest in an interstellar context. 

Different leaders, but not pops, can be gendered male, female, or non-binary (“indeterminate”)/agendered. These are effectively descriptors; as far as I know, they don’t do anything aside from alter the pronoun of the subject leader. I think this leaves an interesting, if restricted, design space. Importantly, however, it left a possible design space for internal politics that felt natural to the game.

Some modders will push existing systems to fit the content of their mod, which is not the design philosophy that I wanted to embrace when crafting this mod; rather, my content should fit in with existing content without feeling out of place or being unintuitive. At the same time, I wanted the flavour of my mod to stand out, to be exciting and unique and be reflected in the mechanics -- which I think I’ve done without straining the systems past their intended design.

I approached this subject matter with care, fully aware of its potential impacts. Stellaris is a game where players can make morally repulsive choices -- enslaving neighboring aliens or their own populace, for example -- but I wanted to avoid trivializing real-world struggles or alienating players. My goal was to create a mod that enhances the game’s storytelling depth while treating sensitive topics with respect and nuance.

I think Stellaris is at its best when it’s allowed to be a lens to explore and engage with complex ideas, and morally scrupulous concepts are definitely not something it shies away from. In my opinion, video games are art in and of themselves; while they usually are a multimedia presentation, the mechanics and code are a unique form of artistic representation not found elsewhere. We can utilize them to further showcase the human experience.

## Technical Aspects

Under the hood, Stellaris mods are written in the Clausewitz scripting language. It’s a domain-specific scripting language that compiles to native code at load time, developed by Paradox Studios for use in their Clausewitz engine -- “Clausewitz” as in Carl von Clausewitz, a Prussian military theorist. You could call Clausewitz a “domain-specific language” or a “compiled language,” and those might be more accurate terms, but for this section I’ve called it a “parsed language”. Compiled felt too broad, domain-specific even moreso, where parsed got the nature of the beast just right.

A parsed scripting language is one where:

- The language has a formal grammar that restricts what can be expressed
- Source code is transformed into an optimized intermediate representation before execution
- The language intentionally trades computational power for predictability/safety
- The parsing step serves as both validation and optimization

Clausewitz is a verbose language. Every parameter is explicitly defined, there’s a heavy use of brackets, and conditional checks read like legal documents. It reminds me of JSON, if JSON were terrible and strongly syntactic and explicitly ordered. Despite this, the language itself is simple. I’ve seen non-programmers comparing it to HTML in ease of learning, which makes for a very healthy modding environment and a strong place for individuals interested in programming or game design to enter the colosseum.

For example, here's a snippet from one of my modded civics, "Patriarchy". The structure seems simple, and it is, but it must be repeated for each civic you wish to introduce. Similar must then be done for government types, and AI personalities, and traits, and so on and so on.

```
civic_patriarchy = {
	icon = "gfx/interface/icons/governments/civics/civic_patriarchy.dds"
	description = "civic_tooltip_genderpolitics_patriarchy_effects"

	potential = {  # "potential" determines if you can view the option
		ethics = {
			NOT = {
				value = ethic_gestalt_consciousness
			}
		}
	}

	possible = {  # "possible" determines if you can select the option
		ethics = {
			NOR = {
				text = civic_tooltip_not_egalitarian
				value = ethic_egalitarian
				value = ethic_fanatic_egalitarian
			}
		}
		origin = {
			NOR = {
				value = origin_necrophage
				value = origin_clone_army
			}
		}
		civics = {
			NOR = {
				text = civic_tooltip_cannot_use_other_gender_civics
				value = civic_matriarchy
				value = civic_reproductive_caste
				value = civic_competitive_courtship
			}
			NOT = {
				value = civic_meritocracy
			}
		}
	}

	random_weight = {
		base = 4
	}

	modifier = {  # "modifier" is the actual in-game effect -- the bonuses or malices it gives you
    country_unity_produces_mult = 0.10
		leader_cost_mult = -0.10
	}
}
```

This dramatically slows down development time, which takes time away from the important bits like design or being with your family. The verbosity is the obvious culprit, but the parsed nature of the language creates other headaches. Because a parsed language also disallows the modification of scripts while the game is running, debugging is particularly time consuming. So you get into this vicious cycle of edit, launch, test, repeat for any minor change you do, until you train yourself for delayed gratification and make a series of changes between each launch (and importantly, you’re tracking those changes so you know what you’re debugging).

When implementing AI personalities (which are implemented separately from government types despite seeming heavily coupled mechanically and conceptually) for example, it can feel like you’re outputting the same templates again and again and again because you are, except you’re tweaking small parameters that you know will impact gameplay in some meaningful way.

LLMs are also poor at implementing Clausewitz, which I found a little strange at first. Surely there must be enough modding resources on the web for Claude to get it right and I can always feed them an explainer. This is for two reasons:

1. it’s esoteric enough that they’re bad at getting the scope right, 
2. a lot of what you’re doing is altering parameters just so which is a goal-oriented process based on the design of the game. 

I shouldn’t yuck them too much here, as they can be good at (2) by translating your design into those parameters, but I found they had a hard time contextualizing what those parameters would do in game and poorly tuned the balance of the mod. Settings could be set much too high -- or usually, much too low! I found good old copy/paste and a mindset for tedium the best solution to this templating problem.

But that verbosity is important to a parsed language. It leaves less room for flexibility, but grants a drastic increase in performance necessary for grand strategy games. As opposed to most other technical aspects of modding Stellaris, parsing is really interesting, so I’m going to dive into it.

I’ll use Lua as a comparison. Lua is an “embedded” language. It runs alongside the game as an interpreter. When a Lua is script is required to execute, the interpreter reads the code, processes it, then performs the requested operations. This flexibility is powerful, as it allows you to add new functions, modify behaviour, and even debug while the game is running.

(Wouldn’t those options have been nice…)

This comes at a performance cost, especially in a game like Stellaris where thousands of calculations occur each game "day" (which might only last milliseconds in real-time, depending on set speed). With an embedded language, the interpreter overhead alone would significantly impact performance.

Clausewitz, as a parsed language, does interpretation upfront. The performance gain from pre-compiling is exceptional, and allows games like Stellaris to exist without slowing to a crawl on modern hardware. The parsed nature of Clausewitz provides another significant advantage: clear error messages. When a script fails to parse at launch, the engine can pinpoint exactly where and why the error occurred, often down to the specific missing bracket or incorrect parameter. This is in stark contrast to embedded languages where errors might only surface during runtime, potentially hours into a playthrough.

Clausewitz also enforces a certain degree of modularity. As long as a script is able to be registered by the Clausewitz engine, which is as simple as naming a `.txt` file specifically, new scripts can easily be added to the game. This natural organization -- which albeit not perfect in the “organizational” aspect -- makes new content easy to add, easy to make compatible with vanilla and other user-created content, and keeps it all easily maintainable.

This modular nature has led to large-scale developments by Paradox modders. See the [Game of Thrones mod for Crusader Kings 2](https://www.moddb.com/mods/crusader-kings-2-a-game-of-thrones-ck2agot) or [Voltaire’s Nightmare for Europa Universalis IV](https://steamcommunity.com/sharedfiles/filedetails/?id=684459310). Both of these are total conversions of the game’s systems, which includes new maps, overhauled mechanics, new AI personalities, entirely new scripted and emergent events, etc. which complexly redesigns the games away from Paradox’s original vision, all as consequence of building with parsed languages.

Are parsed scripts useful outside this context? Absolutely. For instance, many state machines could be called parsed languages. Configuration management tools like Ansible and Puppet use parsed languages to define system states and transitions. These tools parse declarative YAML or custom syntax files that specify desired system configurations, much like how Clausewitz parses game state definitions. The benefits are similar: predictable behavior, clear error messages during parsing, and efficient execution.

Django, a framework I’m familiar with, utilizes parsed scripting in its template language. It is intentionally restricted. You can’t execute arbitrary Python or perform complex operations directly within templates. Templates are parsed at runtime into an optimized form, much like Clausewitz pre-processes scripts at launch. This allows Django to serve hundreds, thousands -- or more -- templates at once.

Database query languages, particularly SQL, share *some* characteristics with parsed languages, but the comparison is more complex. While SQL queries are parsed and validated before execution, modern database engines employ sophisticated query optimizers that go far beyond simple parsing. These optimizers analyze table statistics, available indexes, and data distribution patterns to generate efficient execution plans. Some databases even use adaptive query processing, adjusting their execution strategy based on runtime conditions. PostgresSQL, for instance, can detect when its initial estimates about data distribution were wrong and revise its strategy on the fly.

While they do cache query plans to avoid repeated parsing overhead (similar to how Clausewitz pre-parses mod scripts), the actual execution model is much more dynamic than a purely parsed language. This hybrid approach allows databases to maintain the benefits of early error detection while still optimizing for real-world performance; SQL really highlights that a parsing language is a tool, rather than a solution in and of itself.

So, if you have a situation where

1. Performance is critical,
2. You’re considering using an embedded language,
3. The scope of operations is limited, and
4. You don’t require dynamic content,

try a parsed language!

You can also take a look at some modern solutions, like LuaJIT, which can be extremely performant even when compared to parsed languages.

For more reading on parsed languages, especially in a video game context, I highly recommend this paper: [Evaluating Lua for Use in Computer Game Event Handling - Oskar Forsslund](https://silo.tips/download/evaluating-lua-for-use-in-computer-game-event-handling-oskar-forsslund#).

## Design Considerations

The first challenge in designing a Stellaris mod concerning gender politics was grappling with the fact that I’m a man. My lived experience and societal position inherently shape my understanding of gender-based oppression, and I needed to ensure these perspectives didn't unconsciously perpetuate harmful stereotypes in the mod's design. This design space has been treaded before by other modders -- in fact, this mod was originally a fork of another gender-based mod, though none of the original code exists (I did reuse visual assets, thank you for those [@Capelett](https://steamcommunity.com/id/Capelett/) on steam). I feel like the design decisions in those other implementations, however, often fell into problematic patterns.

Previous mods tended to directly transpose real-world gender dyanmics into the game, essentially recreating familiar patterns of oppression without question why these specific forms would emerge in radically different societies (we're dealing with aliens here). More concerningly, they often reduced complex social structures and caricaturized men and women rather than reflecting or critiquing gender-based oppression. These sterotypes not only oversimplify human gender relations, but make even less sense when applied to alien species that might have entirely different biological and social structures. Empires can also be multi-species, or “xenophilic”. If you have, for example, an immigrating species of “preternaturally strong, preternaturally smart all-female bees” or some such, it becomes very difficult for your empire to support a notion of biology-based sexism. It *must* arise systematically. 

In fact, the imposition of binary gender categories on alien species overlooks the possibility of entirely different or fluid gender systems. Why assume that alien biology or culture would parallel human constructs of "male" and "female"? Some species might have multiple genders, indeterminate genders, or none at all -- many of these configurations exist in Earthen nature already. Clownfish, for example, are naturally genderfluid. They will change sex based on their role in their social group. More striking is a little protozoan *Tetrahymena thermophila* which has seven -- seven! -- different mating types, which is very different from the two that most other eukaryotes have. It's not even an even number! While this design space is exceedingly interesting and stronly implies alien species would not so casually follow a sexual binary, Stellaris imposes a sexual binary on us. Indeterminate gender exists, but it is species-wide, and I haven't found a solid design space for it yet.

Instead of replicating Earth's historical gender patterns, I designed systems to explore how power structures around gender might manifest in interstellar societies. The Patriarchy and Matriarchy civics in my mod exemplify this approach, presenting distinct but mirrored forms of gender authoritarianism. Neither is strictly "better" or "worse," and both avoid gender essentialism—making no assumptions about biological dimorphism or inherent capabilities. Instead, these civics reflect societal dynamics and legal structures, emphasizing that systemic oppression stems from power hierarchies rather than biology.

### Stellaris Terminology
<details><summary>Civic</summary>A policy or ideological characteristic that defines how an empire is governed or structured. Civics reflect an empire's social and political systems, such as a meritocracy or a military junta. They shape gameplay by providing specific bonuses, restrictions, and unique interactions, adding depth to an empire’s roleplay and mechanics.</details>

<details><summary>Government</summary>The overarching framework that dictates how decisions are made in an empire. A government combines an empire's authority type (e.g., democratic, oligarchic) with selected civics to form its unique governing structure. It determines key elements like leadership succession and special bonuses.</details>

<details><summary>Species</summary>The biological group that represents the population of an empire. Species have distinct traits and characteristics, influencing how they interact with the galaxy. They can vary widely, ranging from humanoid to completely alien lifeforms with unique physical and social properties.</details>

<details><summary>Trait</summary>An inherent characteristic of a species that affects its abilities and behaviors. Traits can be biological (e.g., strong, intelligent) or societal (e.g., industrious, charismatic). They provide bonuses or penalties and play a key role in defining a species’ identity and gameplay style.</details>

### Mod Design

The Patriarchy and Matriarchy civics in my mod illustrate how systemic power structures might manifest. Each civic provides gameplay effects that reflect their ideological underpinnings without making essentialist claims about biology. While gender oppression in real life is deeply rooted in societal norms and legal frameworks, Stellaris provides space to explore these ideas through mechanics that remain accessible to various species configurations.

<img src="/images/blog/patriarchy-civic-v0.5.0.png" alt="patriarchy civic" class="civic-image" />
<img src="/images/blog/matriarchy-civic-v0.5.0.png" alt="matriarchy civic" class="civic-image" />

Because I needed for these civics to not be gender essentialist. As gender oppression exists in real life, my civics (core policy of a government in Stellaris) must be exclusively social dynamics or codified in law. Besides that point, there is a designated game space for sexual dimorphism in species traits, but we’ll touch on that later.

This civilization-wide oppression manifests mechanically through the leader trait system. As Stellaris doesn’t have gender designations for individual pops, leaders had to be the target of focus. I felt this restriction actually suited my design goals. Leaders represent individuals who have risen to positions of power within society:

  - leading scientists
  - governors, the heads of worlds or sectors
  - admirals, who head your fleets
  - rulers, the president or grand chancellor or some other supreme authority in your empire.

These leader placements are perfect vessels for examining how gender-based power structures affect social mobility and career advancement. The real distinction in how these civics manifest comes through their effects on leader development and advancement. Rather than making essentialist claims about capability, the mechanics revolve around systemic advantages and barriers.

Leaders of the privileged gender receive a trait granting increased experience gain -- very heavy experience gain, actually, which representing the increased opportunity, trust, access to formal and informal networks, and other accumulated advantages of a system built to support their advancement. Conversely, leaders of the oppressed gender acquire a "glass ceiling" trait that actively hinders their progress and makes them more expensive to recruit; a mechanical representation of systemic barriers rather than any inherent limitation.

The experience modifier for oppressed leaders is deliberately modest. I even toyed with having no modifier, but in my beta I so far think having some trait representing disenfranchisement is necessary. The primary pressure to select privileged-gender leaders shouldn’t come from punishing the selection of oppressed leaders, but from the stark advantages granted to their privileged counterparts. This creates an intuitive pressure that mirrors how systemic advantages often manifest, not through explicit restrictions but through the compounding effects of preferential treatment. This isn’t entirely player-led, as having rulers of the oppressed gender will create a minor amount of instability as well -- perhaps enough to tip the scales toward a more egalitarian configuration!

My mod currently doesn't deal with this, but resistance should naturally arise from these oppressive systems, as well. I have yet to focus on this aspect, but it will be part of moving this mod from Beta^TM to Full Release^TM. Because I haven't developed those systems yet I don't want to talk about them too much, but I'd like events for oppressed gender leaders, wars of emancipation, advanced alien empires exemplifying resistance, and so on.

Creating naturalistic mechanics also meant considering how these systems would interact with the game's other elements. A patriarchal or matriarchal society should feel distinct not just in its leader mechanics, but in how it approaches diplomacy, internal politics, and even war. This means adding unique event chains and diplomatic options that emerge organically from these power structures (though this isn’t a part of my beta version -- I’ve so far only included opinion modifiers between empires, e.g. gender fundamentalists will hold enmity toward gender egalitarian empires).

One interesting aspect of these power structures is how they manifest differently across government types. A democratic matriarchy functions somewhat differently from an imperial one, reflecting how gender-based power dynamics can take distinct forms under different political systems. In democratic matriarchies, for instance, the mechanics emphasize electoral advantages for female candidates, while imperial variants implement a matrilineal succession system, but both ultimately serve to concentrate power along gender lines.

### Species Traits & Essentialism

I tried to be particularly careful with the species trait system. I wanted to explore biological diversity without falling into deterministic traps; it should be possible, in an egalitarian society, for either to prosper given the proper societal support. That gave me two tangential objectives: to meaningfully replicate nature and nature alone, and to avoid simply using numerical modifiers. The latter was a necessary restriction. Mechanically, it is difficult to have modifiers that represent sexual dimorphism. However, dimorphism also allows for exploring some complex sociological interactions.

The “clutch bearer” trait exemplifies how biology and societal structure can intersect without falling into deterministic traps. On its surface, the trait is simple: populations experience cyclical periods of intense reproduction, accompanied by shifts in resource consumption and productivity. While this biological reality introduces practical considerations, such as resource planning and population growth management, it also serves as a foundation for more complex societal dynamics.

To illustrate, I introduced the “Clutch Congress” government type, which explicitly ties the clutch-bearing cycle to the democratic process. In this system, election seasons are synchronized with clutch seasons, both operating on a decade-long cycle and triggered by the death of a ruler. During clutch season, the trait grants women a marginal electoral advantage. The reasoning is rooted in societal trust: women are culturally seen as more capable stewards during this critical time. However, this advantage does not emerge from inherent qualities of clutch bearers but from the deliberate alignment of societal and biological rhythms.

This creates a fascinating feedback loop. The synchronization of elections with clutch seasons systematically privileges certain candidates, reinforcing existing power structures. This mirrors real-world examples where inheritance laws or cultural narratives about gender roles reinforced systemic imbalances, often using biological realities as justification for societal hierarchies; it isn't biological inevitability, but an unfortunate result of how the society has structured itself.

This design was particularly challenging. I had to acknolwedge biological factors without falling into the trap of essentialism -- something I had avoided until this point and was still determined to avoid. While the “Clutch Congress” ties electoral advantages to reproductive cycles, these dynamics are framed as societal choices that amplify their visibility and influence during clutch season. The alignment of clutch season and election season reflects cultural decisions made by the empire, not inherent qualities of clutch-bearers themselves. Herein, I can demonstrate an intersectional play of biology and societal structure rather than claiming this is a preordained outcome of a species that naturally produces clutches.

These design choices aim to create a framework for exploring gender politics that respects both the game's existing systems and the complexity of the subject matter. By working within Stellaris's established mechanics while thoughtfully expanding them, I feel the mod adds depth to the game's storytelling capabilities without forcing specific interpretations or outcomes. As this mod evolves, I hope to delve further into resistance movements and multi-faceted systems of power, creating an even richer space for players to explore these critical themes -- for better or for ill.

## Conclusion

I set out to do two things with this article: describe my mod and talk about some of the considerations of the design details. Somehow it evolved into an exploration of how programming enables storytelling and the technical architecture that makes certain forms of storytelling possible. The parsed language approach of Clausewitz, despite its quirks, is a fantastic foundation for modders to build on that’s both performant and accessible.

Ideally, I’ve gotten across the sensitive nature of this content; an enormous amount of care went into how I wanted to present the subject matter of this mod and I hope that was reflected properly in this article.

I didn’t really get into *how* to create a Stellaris mod in this article, which might have been my intent. That’s okay, though. There’s lots of articles out there about that. The Stellaris wiki is also a great resource. My recommendation, should you choose to start, is pick a small mod you like and try to fork it -- that is, download the mod and look at what it’s doing, then modify that in some way. Stand on the shoulders of giants.

When the mod itself is ready, I’ll write up a mod showcase. Thank you for reading!