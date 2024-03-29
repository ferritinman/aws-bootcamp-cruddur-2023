-- this file was manually created
INSERT INTO public.users (display_name, handle, email, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrewbrown', 'andrew@brown.com','MOCK'),
  ('Andrew Bayko', 'bayko', 'andrew@bayko.com', 'MOCK'),
  ('Ferritin Man', 'ferritin_man', 'ferrittin@man.com', 'MOCK');


INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  ),
  (
    (SELECT uuid from public.users WHERE users.handle = 'bayko' LIMIT 1),
    'I am the other!',
    current_timestamp + interval '10 day'
  );
