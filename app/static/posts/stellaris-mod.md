---
title: Writing a Stellaris Mod
summary: The process of getting my mod, Gender Diversity & Politics, to release. Game design, my careful considerations, and getting sidetracked with parsing.
date: 2024-12-28
tags: gamedev,architecture
toc: true
---


## Introduction
Stellaris is a science fiction story simulator developed by Paradox Studios and published by its parent company, Paradox Interactive. Technically, the niche it occupies is grand strategy with elements of the 4X genre, the “explore, expand, exploit, exterminate” that the Civilization series made famous, but I think that description does it a disservice. It’s more similar to Dwarf Fortress or EVE online where a story emerges out of the latent space created by the game’s mechanics and player(s)‘s imagination and ingenuity, even more so than its sister games, Crusader Kings, Hearts of Iron, et al.

The player becomes the “soul of the nation” of a fledgling interstellar empire taking their first steps outside of their home star system. This soular role is like playing as a collective unconsciousness of a nation, a ghost in the machine directing your nation’s whims; you, the player, select your expansion targets, you react to emergent or scripted events, you conduct diplomacy with aliens states, but it never feels like you’re fully in control. 

The individuals (or “pops”) and leaders in your nation have thoughts and beliefs of their own — represented by game mechanics like happiness and faction support — that are influenced by the actions you take as the nation. Different government types present this concept in different ways; a hive-minded rogue AI will give you more direct control over the citizenry, while a Star Trek-like direct democracy makes individual citizens more powerful. Regardless of government or species or other factors, the player’s influence remains the dominant force.

Recently, I played a game as a direct democracy of humans, who had been given FTL and other future technology by an alien corporation. That allowed the new “Sol Foundation” to begin spreading to the stars, curing cancer, defeating aging — the works. But, my humans owed a massive debt to the corporation, tanking our economy and spurring xenophobia. There was no reason for the terms of our agreement to be so outrageous. These aliens were simply taking advantage of a nascent interstellar nation. 

As the Sol Foundation embarked to the stars, they were aggressive and antagonistic toward other alien civilizations. Their first encounter had been so negative, why shouldn’t the others? But their galactic neighbours were peaceable and kind. There were other threats to deal with than some rowdy humans, who weren’t the worst thing in the south-west quadrant of the galaxy by a mile. They routinely extended trade offers and defensive pacts, which by realpolitik the Sol Foundation would be foolish to not accept and slowly, so slowly, they began to unwind the decades, centuries, of anti-alien attitude. It came to a head when another nation affected by the corporation reached out with something unheard of: a migration treaty, allowing for free movement between their nations. The human’s core xenophobia was coming undone.

This is one of my favourite parts of Stellaris, the internal affairs of your nation outside of economics. It is sadly an underutilized and under-explored aspect in the base game and its expansions (which I’ll call “vanilla” from now on). There are very few instances of internal politics affecting your empire. But this playthrough made me think of what other pieces of internal politics could be improved on from vanilla.

One particular aspect that is lacking but has some support is gender politics. Different leaders, but not pops, can be gendered male, female, non-binary (“indeterminate”), or agendered. These are effectively descriptors; as far as I know, they don’t do anything aside from alter the pronoun of the subject leader. I think this leaves an interesting, if restricted, design space. Importantly, however, it left a possible design space for internal politics that felt natural to the game. 

Some modders will push existing systems to fit the content of their mod, which is not the design philosophy that I wanted to embrace when crafting this mod; rather, my content should fit in with existing content without feeling out of place or being unintuitive. At the same time, I wanted the flavour of my mod to stand out, to be exciting and unique and be reflected in the mechanics — which I think I’ve done without straining the systems past their intended design.

I wanted to tread lightly with this subject matter while also acknowledging the potential impacts. Stellaris is a game where you can enslave the neighbouring aliens — your own populace, even — or do worse, if you so choose, but I didn’t want to be in a position where I would alienate players or trivialize real world struggles. The goal is to create something that enriches the game’s storytelling power while remaining respectful and tasteful. 

I think Stellaris is at its best when it’s allowed to be a lens to explore and engage with complex ideas, and morally scrupulous concepts are definitely not something it shies away from. In my opinion, video games are art in and of themselves; while they usually are a multimedia presentation, the mechanics and code are a unique form of artistic representation not found elsewhere. We can utilize them to further showcase the human experience.

## Technical Aspects

Under the hood, Stellaris mods are written in the Clausewitz scripting language. It’s a domain-specific scripting language that compiles to native code at load time, developed by Paradox Studios for use in their Clausewitz engine — “Clausewitz” as in Carl von Clausewitz, a Prussian military theorist. You could call Clausewitz a “domain-specific language” or a “compiled language,” and those might be more accurate terms, but for this section I’ve called it a “parsed language”. Compiled felt too broad, domain-specific even moreso, where parsed got the nature of the beast just right.

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

This dramatically slows down development time, which takes time away from the important bits like design or being with your family. The verbosity is the obvious culprit, but the parsed nature of the language creates other headaches. A parsed language also disallows the modification of scripts while the game is running, which means debugging is particularly time consuming. So you get into this vicious cycle of edit, launch, test, repeat for any minor change you do, until you train yourself for delayed gratification and make a series of changes between each launch (and importantly, you’re tracking those changes so you know what you’re debugging).

When implementing AI personalities (which are implemented separately from government types despite seeming heavily coupled mechanically and conceptually) for example, it can feel like you’re outputting the same templates again and again and again because you are, except you’re tweaking small parameters that you know will impact gameplay in some meaningful way. 

LLMs are also poor at implementing Clausewitz, which I found a little strange at first. Surely there must be enough modding resources on the web for Claude to get it right and I can always feed them an explainer. This is for two reasons:

1. it’s esoteric enough that they’re bad at getting the scope right, 
2. a lot of what you’re doing is altering parameters just so which is a goal-oriented process based on the design of the game. 

I shouldn’t yuck them too much here, as they can be good at (2) by translating your design into those parameters, but I found they had a hard time contextualizing what those parameters would do in game and poorly tuned the balance of the mod. Settings could be set much too high — or usually, much too low! I found good old copy/paste and a mindset for tedium the best solution to this templating problem.

The verbosity is important, however, to Clausewitz. It is a “parsed” language as opposed to an embedded scripting language that might be more familiar, such as Lua. This leaves less room for flexibility, but grants a drastic increase in performance in event-based systems (such as a grand strategy game). As opposed to most other aspects of modding, this bit is really technically interesting, so let me dive into it.

I’ll continue using Lua as a comparison. Lua is an “embedded” language. It runs alongside the game as an interpreter. When a Lua is script is required to execute, the interpreter reads the code, processes it, then performs the requested operations. This flexibility is powerful, as it allows you to add new functions, modify behaviour, and even debug while the game is running.

(Wouldn’t those options have been nice…)

This comes at a performance cost, especially in a game like Stellaris where thousands of calculations occur each game "day" (which might only last milliseconds in real-time, depending on set speed). With an embedded language, the interpreter overhead alone would significantly impact performance.

Clausewitz takes a different approach. When the game launches, all scripts are parsed and converted into an optimized format that the engine can efficiently process. This means that while you're playing, there's no interpretation overhead The engine knows exactly what each script does and can execute it with minimal processing. Think of it like the difference between having a real-time translator (Lua) versus reading from a pre-translated book (Clausewitz). You can't change the translation on the fly, but you can read it instantly.

The performance gain from pre-compiling is exceptional, and allows games like Stellaris to exist without slowing to a crawl on modern hardware. The parsed nature of Clausewitz provides another significant advantage: clear error messages. When a script fails to parse at launch, the engine can pinpoint exactly where and why the error occurred, often down to the specific missing bracket or incorrect parameter. This is in stark contrast to embedded languages where errors might only surface during runtime, potentially hours into a playthrough.

Clausewitz also enforces a certain degree of modularity. As long as a script is able to be registered by the Clausewitz engine, which is as simple as naming a `.txt` file specifically, new scripts can easily be added to the game. This natural organization — which albeit not perfect in the “organizational” aspect — makes new content easy to add, easy to make compatible with vanilla and other user-created content, and keeps it all easily maintainable.

This modular nature has led to large-scale developments my Paradox modders. See the [Game of Thrones mod for Crusader Kings 2](https://www.moddb.com/mods/crusader-kings-2-a-game-of-thrones-ck2agot) or [Voltaire’s Nightmare for Europa Universalis IV](https://steamcommunity.com/sharedfiles/filedetails/?id=684459310). Both of these are total conversions of the game’s systems, which includes new maps, overhauled mechanics, new AI personalities, entirely new scripted and emergent events, etc. which complexly redesigns the games away from Paradox’s original vision, all as consequence of building with parsed languages.

Are parsed scripts useful outside this context? Absolutely. For instance, many state machines could be called parsed languages. Configuration management tools like Ansible and Puppet use parsed languages to define system states and transitions. These tools parse declarative YAML or custom syntax files that specify desired system configurations, much like how Clausewitz parses game state definitions. The benefits are similar: predictable behavior, clear error messages during parsing, and efficient execution.

Django, a framework I’m familiar with, utilizes parsed scripting in its template language. It is intentionally restricted. You can’t execute arbitrary Python or perform complex operations directly within templates. Templates are parsed at runtime into an optimized form, much like Clausewitz pre-processes scripts at launch. This allows Django to serve hundreds, thousands — or more — templates at once.

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

The first challenge in designing a Stellaris mod concerning gender politics was grappling with the fact that I’m a man. My lived experience and societal position inherently shape my understanding of gender-based oppression, and I needed to ensure these perspectives didn't unconsciously perpetuate harmful stereotypes in the mod's design. This design space has been treaded before by other modders -- in fact, this mod was originally a fork of another gender-based mod, though none of the original code exists (I did reuse visual assets, thank you for those @Capelett on steam). I feel like the design decisions in those other implementations, however, often fell into problematic patterns.

Previous mods tended to directly transpose real-world gender dyanmics into the game, essentially recreating familiar patterns of oppression without question why these specific forms would emerge in radically different societies (we're dealing with aliens here). More concerningly, they often reduced complex social structures and caricaturized men and women rather than reflecting or critiquing gender-based oppression. These sterotypes not only oversimplify human gender relations, but make even less sense when applied to alien species that might have entirely different biological and social structures.

Instead, I wanted to create systems that explored how power structures could manifest around gender without being bound by Earth's specific historical patterns. Take the Patriarchy and Matriarchy civics in my mod: rather than making one strictly "better" or "worse," they represent different approaches to gender authoritarianism that mirror each other in key ways. I needed for these civics to not be gender essentialist -- that is, they couldn't make any claims about possible dimorphism or the biology of a species. As gender oppression exists in real life, my civics (core policy of a government in Stellaris) must be exclusively social dynamics or codified in law.

TODO
[This manifests mechanically through the leader trait system. Both civics provide identical base benefits: increased unity production and reduced leader recruitment costs.]

<img src="/static/images/blog/patriarchy-civic-v0.5.0.png" alt="patriarchy civic" class="civic-image" />
<img src="/static/images/blog/matriarchy-civic-v0.5.0.png" alt="matriarchy civic" class="civic-image" />

[The real distinction comes from how they affect leader development through traits. Leaders of the privileged gender gain experience faster, while those of the oppressed gender face a "glass ceiling" trait that actively hinders their advancement and increases their cost. This mechanical implementation avoids making claims about innate capabilities - instead, it purely represents systemic advantages and barriers.]


- should talk about the challenge of making the mod feel “naturalistic” and what goes into that

## Conclusion

I set out to do two things with this article: describe my mod and talk about some of the considerations of the design details. Somehow it evolved into an exploration of how programming enables storytelling and the technical architecture that makes certain forms of storytelling possible. The parsed language approach of Clausewitz, despite its quirks, is a fantastic foundation for modders to build on that’s both performant and accessible.

Ideally, I’ve gotten across the sensitive nature of this content; an enormous amount of care went into how I wanted to present the subject matter of this mod and I hope that was reflected properly in this article.

I didn’t really get into *how* to create a Stellaris mod in this article, which might have been my intent. That’s okay, though. There’s lots of articles out there about that. The Stellaris wiki is also a great resource. My recommendation, should you choose to start, is pick a small mod you like and try to fork it — that is, download the mod and look at what it’s doing, then modify that in some way. Stand on the shoulders of giants.

When the mod itself is ready, I’ll write up a mod showcase. Thank you for reading!