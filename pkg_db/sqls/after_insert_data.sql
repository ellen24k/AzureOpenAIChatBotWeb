create or replace function after_insert_data() returns trigger
    language plpgsql
as
$$
BEGIN
    RAISE NOTICE 'New row inserted %', NEW.date;

    RAISE LOG '[after_insert_data] 트리거가 실행되었습니다.';
    PERFORM update_moved_status_default_image();
    RAISE LOG '[after_insert_data] update_moved_status... 실행되었습니다.';
    PERFORM request_edge_function_chatbot_dalle_image_batch_processor();
    RAISE LOG '[after_insert_data] request_edge_function... 실행되었습니다.';
RETURN NEW;
END;
$$;

alter function after_insert_data() owner to postgres;

grant execute on function after_insert_data() to anon;

grant execute on function after_insert_data() to authenticated;

grant execute on function after_insert_data() to service_role;

