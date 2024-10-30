-- request history
select * from net._http_response;

-- 트리거 생성
create trigger after_insert_data_trigger
    after insert
    on data
    for each row
    execute procedure after_insert_data();

