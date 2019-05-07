CREATE TYPE public.response AS
   (
        message text,
        type character varying,
        data json
    );