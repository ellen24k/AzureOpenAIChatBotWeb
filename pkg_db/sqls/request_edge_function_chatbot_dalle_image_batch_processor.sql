-- dashboard에서 extension on 해줄 것
CREATE EXTENSION IF NOT EXISTS pg_net;

create or REPLACE function request_edge_function_chatbot_dalle_image_batch_processor() returns json
    language plpgsql
as
$$
DECLARE
response json;
    function_url text := 'https://???.supabase.co/functions/v1/???';
--     headers json := json_build_object('Authorization', 'Bearer eyJhbG...');
    data json := json_build_object('name', 'Functions');
    request_id int;
BEGIN
    PERFORM net.http_post(
            function_url,
            data::JSONB,
            headers := '{"Authorization": "Bearer eyJhbG..."}'::JSONB
            ) as request_id;


--     -- 요청 및 응답 정보를 로그로 출력합니다.
--     RAISE NOTICE 'Request URL: %', function_url;
--     RAISE NOTICE 'Request Headers: %', headers;
--     RAISE NOTICE 'Request Data: %', data;
--     RAISE NOTICE 'Status Code: %', response->>'status';
--     RAISE NOTICE 'Response: %', response;
--
--     -- 상태 코드가 200이 아닌 경우 오류 메시지를 출력합니다.
--     IF response->>'status' != '200' THEN
--         RAISE EXCEPTION 'Error invoking function: %', response->>'message';
--     END IF;

--     RETURN response;

RETURN json_build_object('request_id', request_id);
END;
$$;

alter function request_edge_function_chatbot_dalle_image_batch_processor() owner to postgres;

grant execute on function request_edge_function_chatbot_dalle_image_batch_processor() to anon;
grant execute on function request_edge_function_chatbot_dalle_image_batch_processor() to authenticated;
grant execute on function request_edge_function_chatbot_dalle_image_batch_processor() to service_role;