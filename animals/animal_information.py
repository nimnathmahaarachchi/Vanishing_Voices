"""Species records: saved estimates, source rules, and profile information.

Slugs connect records to pages, maps, and photographs. HTML profile text is edited
separately, so keep its saved figures and descriptions in sync with these records.
"""

# Patterns and numeric bounds define what each source check can accept.
ANIMALS = [

    {'slug': 'tiger',  # The short ID used in URLs and lookups; the other records use the same fields.
     'name': 'Tiger',
     'scientific': 'Panthera tigris',  # The scientific name displayed beside the common name.
     'status': 'EN',  # EN means endangered; CR means critically endangered.
     'region': 'Asia',
     'habitat': 'Forests & grasslands',
     'location': 'South, Southeast & East Asia',
     'coordinate': [80.6, 22.2],  # Longitude first, then latitude; this represents one habitat location.
     'pin': 'Central India · representative habitat',
     'population': '5,711',  # Saved display text; it can also contain a range, <, or an approximate sign.
     'unit': 'estimated wild tigers',  # Explain what was counted; not every source counts the same group.
     'estimate_date': '2025 estimate',  # The date attached to the estimate, separate from our source review date.
     'source_name': 'WWF-UK',
     'source_url': 'https://www.wwf.org.uk/learn/wildlife/tigers',
     'pattern': 'numbers are now on the rise at\\s*([\\d,]+)\\s*in\\s*(20\\d{2})',  # Capture the population and year from the expected source sentence.
     'format': 'number',  # Choose the display style: number, range, less, or approx.
     'minimum': 1000,  # The smallest acceptable extracted value; smaller values need review.
     'maximum': 20000,  # The largest acceptable extracted value; this is a parser check, not a forecast.
     'tagline': 'Tigers depend on connected habitats and sufficient prey.',
     'intro': 'The tiger  is the largest Asian cat. Individuals can be identified by their stripe patterns, '
              'which are used in camera-trap research.',
     'where': 'Wild tigers  occur in separated populations across Asia. Their range includes India and Nepal, '
              'with other populations in the Russian Far East and Sumatra. The marker indicates central India. '
              'Connected habitat and access to water support their survival.',
     'happened': 'Poaching for skins and body parts has contributed to population decline. Forest conversion '
                 'reduces available habitat, while roads can divide populations and restrict movement. Prey '
                 'depletion creates further pressure.',
     'hope': 'Protected areas and habitat corridors support recovery in some regions. Community conservation '
             'programmes and anti-poaching patrols also contribute. National trends differ, so an increase in '
             'the global estimate can coexist with local declines.',
     'threats': ['Habitat fragmentation', 'Illegal wildlife trade', 'Loss of prey'],
     'fact': 'A tiger’s stripe pattern is as individual as a fingerprint.',
     'population_note': 'WWF-UK reports 5,711 wild tigers for 2025. A global estimate combines national surveys '
                        'made using different methods and in different years; it is not a live census.',
     'help_name': 'WWF-UK conservation information',
     'help_url': 'https://www.wwf.org.uk/learn/wildlife/tigers',
     'reviewed_on': '2026-10-22'},  # When this saved record was reviewed, not the date of a new animal census.

    {'slug': 'amur-leopard',
     'name': 'Amur leopard',
     'scientific': 'Panthera pardus orientalis',
     'status': 'CR',
     'region': 'Asia',
     'habitat': 'Temperate forests',
     'location': 'Russian Far East & northeast China',
     'coordinate': [131.1, 43.4],
     'pin': 'Primorye · Russia–China border region',
     'population': '≈130',
     'unit': 'estimated mature individuals',
     'estimate_date': '2023 estimate · cited by WWF-UK',
     'source_name': 'WWF-UK',
     'source_url': 'https://www.wwf.org.uk/learn/wildlife/amur-leopards',
     'pattern': 'increased to around\\s*([\\d,]+)\\s*adults',
     'format': 'approx',
     'minimum': 20,
     'maximum': 2000,
     'tagline': 'The remaining population occupies forests near the Russia–China border.',
     'intro': 'The Amur leopard  has a thick coat adapted to cold conditions. It is a solitary cat that uses '
              'forested slopes in the northern part of the leopard range.',
     'where': 'The remaining wild  population is concentrated in the Russian Far East and northeast China. '
              'Forest connections allow movement between protected areas. These habitats also support the prey '
              'on which the leopards depend.',
     'happened': 'Hunting for fur and forest fragmentation reduced the population. Poaching of prey adds '
                 'pressure because suitable habitat must contain enough food. Losses among breeding adults '
                 'affect a population of this size.',
     'hope': 'Cross-border habitat protection supports recovery. Camera traps provide evidence of population '
             'changes, while wildlife-crime control reduces direct threats. Conservation work also protects the '
             'prey base.',
     'threats': ['Poaching', 'Forest loss', 'Prey scarcity'],
     'fact': 'Its long tail can be held around the body in cold weather.',
     'population_note': 'WWF-UK cites an estimate of around 130 mature individuals in 2023. Mature individuals '
                        'are a different measure from all ages combined.',
     'help_name': 'WWF-UK conservation information',
     'help_url': 'https://www.wwf.org.uk/learn/wildlife/amur-leopards',
     'reviewed_on': '2026-10-22'},

    {'slug': 'asian-elephant',
     'name': 'Asian elephant',
     'scientific': 'Elephas maximus',
     'status': 'EN',
     'region': 'Asia',
     'habitat': 'Forests & grasslands',
     'location': 'South & Southeast Asia',
     'coordinate': [100.5, 15.3],
     'pin': 'Thailand · representative habitat',
     'population': '<52,000',
     'unit': 'estimated wild elephants',
     'estimate_date': 'Source reviewed January 2026',
     'source_name': 'WWF-UK',
     'source_url': 'https://www.wwf.org.uk/learn/wildlife/asian-elephant',
     'pattern': 'fewer than\\s*([\\d,]+)\\s*Asian elephants left in the wild',
     'format': 'less',
     'minimum': 10000,
     'maximum': 100000,
     'tagline': 'Habitat fragmentation restricts elephant movement across Asia.',
     'intro': 'Asian elephants live in  social groups and disperse seeds across their habitats. Their movement '
              'can create routes through vegetation that are used by other animals.',
     'where': 'Asian elephants occur in  fragmented populations across South and Southeast Asia, including '
              'southern China. Forests and grasslands are used, and some routes change with seasonal food '
              'availability. The marker indicates a representative location in Thailand.',
     'happened': 'Agricultural expansion and settlements have divided elephant habitat. Roads create further '
                 'barriers. Conflict can occur when elephants enter cultivated areas, and poaching remains an '
                 'additional threat.',
     'hope': 'Habitat corridors allow movement between separated areas. Land-use planning can reduce conflict '
             'with nearby communities, while early-warning systems support local responses. Habitat restoration '
             'provides another means of improving access between feeding areas.',
     'threats': ['Habitat fragmentation', 'Human–wildlife conflict', 'Poaching'],
     'fact': 'Elephants help forests regenerate by carrying seeds across the landscape.',
     'population_note': 'WWF-UK reports fewer than 52,000 in the wild. Its page was reviewed in January 2026; '
                        'this is a page review date, not a new census date. The underlying estimate year is not '
                        'stated.',
     'help_name': 'WWF-UK conservation information',
     'help_url': 'https://www.wwf.org.uk/learn/wildlife/asian-elephant',
     'reviewed_on': '2026-10-22'},

    {'slug': 'black-rhino',
     'name': 'Black rhinoceros',
     'scientific': 'Diceros bicornis',
     'status': 'CR',
     'region': 'Africa',
     'habitat': 'Savannas & shrublands',
     'location': 'Eastern & southern Africa',
     'coordinate': [18, -20],
     'pin': 'Namibia · representative habitat',
     'population': '6,788',
     'unit': 'estimated wild rhinos',
     'estimate_date': 'End of 2024 · reported in 2026',
     'source_name': 'International Rhino Foundation',
     'source_url': 'https://rhinos.org/about-rhinos/state-of-the-rhino/',
     'pattern': 'black rhinos increased from\\s*[\\d,]+\\s*in\\s*20\\d{2}\\s*to\\s*([\\d,]+)\\s*at the end '
                'of\\s*(20\\d{2})',
     'format': 'number',
     'minimum': 1000,
     'maximum': 30000,
     'tagline': 'Population recovery remains dependent on protection from poaching.',
     'intro': 'The black  rhinoceros browses leaves and twigs with a pointed upper lip. Its body is usually '
              'grey, despite the common name.',
     'where': 'Wild populations  remain in eastern and southern Africa. Namibia and South Africa contain '
              'important populations; Kenya and Zimbabwe also form part of the range. The map marker represents '
              'habitat in Namibia.',
     'happened': 'Poaching for horn caused substantial population losses. Demand in the illegal horn trade '
                 'continues to affect the species. Habitat pressure also limits the areas available for '
                 'recovery.',
     'hope': 'Protection programmes and managed translocations have supported population growth. Community '
             'conservation contributes to this work. The International Rhino Foundation report published in 2026 '
             'repeats an estimate of 6,788 animals at the end of 2024.',
     'threats': ['Illegal horn trade', 'Poaching', 'Habitat pressure'],
     'fact': 'Its pointed upper lip is adapted to picking leaves from shrubs.',
     'population_note': 'The 2026 State of the Rhino report repeats an estimate of 6,788 black rhinos at the end '
                        'of 2024. The report year and population year are deliberately shown separately.',
     'help_name': 'International Rhino Foundation conservation information',
     'help_url': 'https://rhinos.org/',
     'reviewed_on': '2026-10-22'},

    {'slug': 'mountain-gorilla',
     'name': 'Mountain gorilla',
     'scientific': 'Gorilla beringei beringei',
     'status': 'EN',
     'region': 'Africa',
     'habitat': 'Montane forests',
     'location': 'Rwanda, Uganda & DR Congo',
     'coordinate': [29.6, -1.4],
     'pin': 'Virunga Mountains · representative habitat',
     'population': '1,063',
     'unit': 'minimum wild gorillas in census',
     'estimate_date': '2015–2018 censuses · announced 2019',
     'source_name': 'Dian Fossey Gorilla Fund',
     'source_url': 'https://gorillafund.org/dian-fossey/bwindi-census/',
     'pattern': '(?:overall total of mountain gorillas is now|total[^.]{0,60}?)\\s*([\\d,]+)',
     'format': 'number',
     'minimum': 500,
     'maximum': 5000,
     'tagline': 'Mountain gorillas survive in two separated forest areas.',
     'intro': 'Mountain gorillas live  in social groups in high-elevation forests. Their recovery has been '
              'associated with sustained conservation work, although threats remain.',
     'where': 'One population occupies  the Virunga Massif across Rwanda, Uganda and the Democratic Republic of '
              'the Congo. The other occupies Bwindi Impenetrable National Park in Uganda and the adjoining '
              'Sarambwe reserve in DR Congo.',
     'happened': 'Forest clearance reduces available habitat. Snares and regional conflict have also affected '
                 'the populations. Close contact with people creates a risk of disease transmission.',
     'hope': 'Daily protection and veterinary care support survival. Conservation programmes also involve '
             'neighbouring communities. Tourism can provide financial support when visitor-distance and health '
             'rules are followed.',
     'threats': ['Habitat loss', 'Disease', 'Snares'],
     'fact': 'Thick fur helps mountain gorillas live in cool, high-elevation forests.',
     'population_note': 'The combined censuses put the minimum at 1,063, announced in 2019. This remains a '
                        'widely cited baseline; it is not a count made in 2026. A refresh checks the named '
                        'report, not an undiscovered new census.',
     'help_name': 'Dian Fossey Gorilla Fund conservation information',
     'help_url': 'https://gorillafund.org/',
     'reviewed_on': '2026-10-22'},

    {'slug': 'sumatran-orangutan',
     'name': 'Sumatran orangutan',
     'scientific': 'Pongo abelii',
     'status': 'CR',
     'region': 'Asia',
     'habitat': 'Tropical rainforests',
     'location': 'Northern Sumatra, Indonesia',
     'coordinate': [97.3, 3.7],
     'pin': 'Leuser landscape · northern Sumatra',
     'population': '11,694',
     'unit': 'estimated wild orangutans',
     'estimate_date': '2021–2023 survey · released July 2026',
     'source_name': 'Indonesia Ministry of Forestry',
     'source_url': 'https://www.kehutanan.go.id/pers/kementerian-kehutanan-ungkap-hasil-survei-terbaru-perkuat-kolaborasi-konservasi-orangutan-sumatera-dan-orangutan-tapanuli',
     'pattern': 'Orangutan Sumatera\\s*\\(Pongo abelii\\)\\s*diperkirakan mencapai\\s*([\\d.]+)\\s*individu',
     'format': 'number',
     'minimum': 1000,
     'maximum': 50000,
     'tagline': 'Connected forest habitat supports Sumatran orangutan populations.',
     'intro': 'Sumatran orangutans spend much  of their lives in the forest canopy. They disperse seeds and '
              'contribute to rainforest regeneration.',
     'where': 'The species occurs on  Sumatra, mainly in the northern forests. The Leuser landscape is an '
              'important habitat. It is classified separately from Bornean and Tapanuli orangutans.',
     'happened': 'Forest conversion removes habitat, and roads can separate remaining groups. Illegal capture '
                 'and killing add to population losses. Recovery is slow because reproduction occurs at long '
                 'intervals.',
     'hope': 'Protection of intact forests is a principal conservation measure. Reconnected habitat can support '
             'movement between isolated areas. Indonesia’s Ministry of Forestry published results from the '
             '2021–2023 surveys in July 2026.',
     'threats': ['Deforestation', 'Habitat fragmentation', 'Illegal capture'],
     'fact': 'Orangutans are important seed dispersers in their rainforest homes.',
     'population_note': 'The Ministry’s July 2026 release reports 11,694 Sumatran orangutans from surveys '
                        'conducted in 2021–2023. This figure applies to Pongo abelii. Tapanuli and Bornean '
                        'orangutans are counted separately.',
     'help_name': 'Sumatran orangutan conservation',
     'help_url': 'https://www.sumatranorangutan.org/',
     'reviewed_on': '2026-10-22'},

    {'slug': 'hawksbill-turtle',
     'name': 'Hawksbill turtle',
     'scientific': 'Eretmochelys imbricata',
     'status': 'CR',
     'region': 'Oceans',
     'habitat': 'Coral reefs',
     'location': 'Tropical Atlantic, Indian & Pacific oceans',
     'coordinate': [-66, 18],
     'pin': 'Caribbean Sea · representative habitat',
     'population': '20,000–23,000',
     'unit': 'estimated nesting females',
     'estimate_date': 'Source estimate · year not stated',
     'source_name': 'Sea Turtle Conservancy',
     'source_url': 'https://conserveturtles.org/species/hawksbill/',
     'pattern': 'Population estimate is between\\s*([\\d,]+)\\s*and\\s*([\\d,]+)\\s*nesting females',
     'format': 'range',
     'minimum': 1000,
     'maximum': 200000,
     'tagline': 'The displayed estimate refers to nesting females.',
     'intro': 'The hawksbill  turtle has a narrow beak adapted to feeding in reef crevices. Its patterned shell '
              'has also made the species a target of the tortoiseshell trade.',
     'where': 'Hawksbills occur  in tropical and subtropical waters of the Atlantic, Indian and Pacific oceans. '
              'Coastal coral reefs are important habitats. A Caribbean location is marked on the map.',
     'happened': 'The shell trade and egg collection have reduced populations. Fishing bycatch causes further '
                 'losses, while coastal development can damage nesting beaches. Changes to reef habitat also '
                 'affect the species.',
     'hope': 'Nesting-beach protection supports reproduction. Bycatch reduction and controls on the shell trade '
             'address other threats. The species feeds heavily on sponges, which links its feeding activity to '
             'reef communities.',
     'threats': ['Illegal shell trade', 'Fishing bycatch', 'Reef & beach loss'],
     'fact': 'Its narrow beak allows access to food in coral crevices.',
     'population_note': 'The estimate covers nesting females. Males and juveniles are outside this measure, as '
                        'are females that do not nest during the period represented. The source does not state '
                        'an estimate year.',
     'help_name': 'Sea Turtle Conservancy conservation information',
     'help_url': 'https://conserveturtles.org/',
     'reviewed_on': '2026-10-22'},

    {'slug': 'blue-whale',
     'name': 'Blue whale',
     'scientific': 'Balaenoptera musculus',
     'status': 'EN',
     'region': 'Oceans',
     'habitat': 'Open ocean',
     'location': 'Oceans worldwide',
     'coordinate': [-75, -39],
     'pin': 'Southeast Pacific · representative habitat',
     'population': '10,000–25,000',
     'unit': 'estimated whales worldwide',
     'estimate_date': 'Source estimate · year not stated',
     'source_name': 'WWF',
     'source_url': 'https://www.worldwildlife.org/species/whale/blue-whale/',
     'pattern': 'Population\\s*([\\d,]+)\\s*[–—−-]\\s*([\\d,]+)',
     'format': 'range',
     'minimum': 1000,
     'maximum': 200000,
     'tagline': 'Blue whale estimates cover populations across several oceans.',
     'intro': 'The blue whale  is the largest living animal. It feeds mainly on krill and travels between '
              'feeding and breeding areas.',
     'where': 'Blue whales occur  in the major oceans. Feeding areas and migration routes differ between '
              'populations. The marker indicates a representative location off Chile in the southeast Pacific.',
     'happened': 'Industrial whaling reduced population numbers substantially. Ship collisions and entanglement '
                 'remain threats. Underwater noise can affect whale behaviour, while changes in ocean conditions '
                 'influence food availability.',
     'hope': 'Ship-strike reduction and noise management address continuing threats. Feeding-habitat protection '
             'is also relevant. Regional surveys and acoustic observations contribute to population research.',
     'threats': ['Ship strikes', 'Ocean noise', 'Entanglement'],
     'fact': 'Blue whales feed mainly on krill.',
     'population_note': 'WWF provides a global estimate of 10,000–25,000 whales. The estimate year is absent '
                        'from the source page. Regional estimates and counts of mature individuals use different '
                        'population definitions.',
     'help_name': 'NOAA blue whale information',
     'help_url': 'https://www.fisheries.noaa.gov/species/blue-whale',
     'reviewed_on': '2026-10-22'},

    {'slug': 'vaquita',
     'name': 'Vaquita',
     'scientific': 'Phocoena sinus',
     'status': 'CR',
     'region': 'Americas',
     'habitat': 'Shallow coastal waters',
     'location': 'Upper Gulf of California, Mexico',
     'coordinate': [-114.7, 30.7],
     'pin': 'Upper Gulf of California · Mexico',
     'population': '7–10',
     'unit': 'animals observed in the 2025 survey',
     'estimate_date': 'May–September 2025 survey',
     'source_name': 'CONANP / Sea Shepherd',
     'source_url': 'https://seashepherd.org/2025/10/28/results-of-the-2025-vaquita-monitoring-effort/',
     'pattern': 'confirming sightings of between\\s*(\\d+)\\s*and\\s*(\\d+)\\s*vaquitas',
     'format': 'range',
     'minimum': 1,
     'maximum': 1000,
     'tagline': 'Gillnet bycatch threatens the remaining vaquita population.',
     'intro': 'The vaquita is a  small porpoise with dark patches around its eyes. Its restricted distribution '
              'places particular importance on protection of the northern Gulf of California.',
     'where': 'Vaquitas occur only in  the northern Gulf of California, Mexico. Fishing takes place within the '
              'same region. Conservation measures therefore require attention to local livelihoods as well as '
              'the remaining animals.',
     'happened': 'Vaquitas can become trapped in gillnets and drown. Illegal nets used for totoaba fishing are '
                 'part of this problem. Repeated bycatch has reduced the population to a very small number.',
     'hope': 'Removal of illegal nets and enforcement of protected areas address the immediate threat. '
             'Alternative fishing methods can reduce bycatch. Calves were recorded during the 2025 monitoring '
             'effort, which provides evidence of continued reproduction.',
     'threats': ['Gillnet bycatch', 'Illegal totoaba fishing', 'Extremely small population'],
     'fact': 'The entire species is native to a small part of Mexico’s Gulf of California.',
     'population_note': 'The 2025 monitoring effort reported sightings of 7–10 vaquitas. This is a survey '
                        'observation estimate, not a complete count of every living animal; some may have been '
                        'outside the surveyed area.',
     'help_name': 'CONANP / Sea Shepherd conservation information',
     'help_url': 'https://seashepherd.org/vaquita/',
     'reviewed_on': '2026-10-22'},

    {'slug': 'kakapo',
     'name': 'Kākāpō',
     'scientific': 'Strigops habroptilus',
     'status': 'CR',
     'region': 'Oceania',
     'habitat': 'Island forests',
     'location': 'Protected islands, Aotearoa New Zealand',
     'coordinate': [166.6, -45.6],
     'pin': 'Fiordland region · approximate recovery habitat',
     'population': '325',
     'unit': 'living birds in the recovery population',
     'estimate_date': 'September 2026 recovery update',
     'source_name': 'NZ Department of Conservation',
     'source_url': 'https://www.doc.govt.nz/our-work/kakapo-recovery/',
     'pattern': 'There are\\s*([\\d,]+)\\s*kākāpō alive today',
     'format': 'number',
     'minimum': 50,
     'maximum': 10000,
     'tagline': 'A managed recovery programme supports the remaining kākāpō.',
     'intro': 'The kākāpō  is a nocturnal, flightless parrot native to New Zealand. Its ground-nesting behaviour '
              'makes it vulnerable to introduced predators.',
     'where': 'Kākāpō occupy  protected recovery sites in Aotearoa New Zealand. Predator-free island habitats '
              'support the managed population. The marker indicates an approximate region to avoid disclosure of '
              'individual bird locations.',
     'happened': 'Introduced predators and habitat loss caused a severe decline. Breeding occurs infrequently, '
                 'which slows population recovery. Continued management is therefore required.',
     'hope': 'Ngāi Tahu and the Department of Conservation work with researchers and programme supporters. Birds '
             'are monitored closely. DOC reported 325 birds in September 2026 after a successful breeding '
             'season.',
     'threats': ['Introduced predators', 'Habitat loss', 'Low breeding frequency'],
     'fact': 'The kākāpō is a nocturnal, flightless parrot.',
     'population_note': 'DOC’s recovery page reports 325 living birds, supported by its September 2026 milestone '
                        'announcement. This closely managed population can change as birds hatch, survive to the '
                        'official count, or die.',
     'help_name': 'NZ Department of Conservation conservation information',
     'help_url': 'https://www.doc.govt.nz/our-work/kakapo-recovery/',
     'reviewed_on': '2026-10-22'},
]
