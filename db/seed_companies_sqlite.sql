-- Seed companies for NucRadar v1 (SQLite)

INSERT OR IGNORE INTO companies (name, slug, type, tech, website) VALUES
  ('TerraPower',        'terrapower',        'reactor',     'SFR + molten salt storage', NULL),
  ('Kairos Power',      'kairos-power',      'reactor',     'FHR demo reactors', NULL),
  ('X-energy',          'x-energy',          'reactor',     'HTGR / Xe-100 + TRISO', NULL),
  ('NuScale Power',     'nuscale',           'reactor',     'LWR SMR (VOYGR)', NULL),
  ('Natura Resources',  'natura-resources',  'reactor',     'MSRR at ACU', NULL),

  ('Radiant',           'radiant',           'microreactor','Kaleidos portable microreactor', NULL),
  ('Aalo Atomics',      'aalo-atomics',      'microreactor','Aalo-1 sodium microreactor', NULL),
  ('Last Energy',       'last-energy',       'microreactor','PWR-like modular microreactor', NULL),
  ('Valar Atomics',     'valar-atomics',     'microreactor','Ward-250 concept', NULL),
  ('Deep Fission',      'deep-fission',      'microreactor','Deep borehole PWR', NULL),
  ('Antares Nuclear',   'antares-nuclear',   'microreactor','Sodium heat-pipe microreactor', NULL),
  ('NANO Nuclear',      'nano-nuclear',      'microreactor','KRONOS / ZEUS concepts', NULL),
  ('Terra Innovatum',   'terra-innovatum',   'microreactor','Helium-cooled microreactor', NULL),

  ('Curio',             'curio',             'fuel',        'NuCycle fuel recycling', NULL),
  ('Standard Nuclear',  'standard-nuclear',  'fuel',        'TRISO fuel fab', NULL),
  ('TRISO-X',           'triso-x',           'fuel',        'TRISO-X fuel fab', NULL),
  ('Nusano',            'nusano',            'fuel',        'Non-centrifuge HALEU process', NULL),
  ('SHINE',             'shine',             'fuel',        'Isotopes + recycled feed', NULL),
  ('Oklo',              'oklo',              'reactor',     'Aurora + fuel center narrative', NULL);
