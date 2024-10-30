create function update_moved_status_default_image() returns integer
    language plpgsql
as
$$
DECLARE
affected_rows integer;
BEGIN
UPDATE data
SET moved = True
WHERE img_url = 'https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/default_img.png';

GET DIAGNOSTICS affected_rows = ROW_COUNT;

RAISE LOG '[update_moved] 업데이트 된 행의 수 %', affected_rows;

    IF affected_rows IS NULL THEN
        RETURN 0;
ELSE
        RETURN affected_rows;
END IF;
END;
$$;

alter function update_moved_status_default_image() owner to postgres;

grant execute on function update_moved_status_default_image() to anon;

grant execute on function update_moved_status_default_image() to authenticated;

grant execute on function update_moved_status_default_image() to service_role;

