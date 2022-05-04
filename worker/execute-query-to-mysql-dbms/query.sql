-- select userNo, userName from user
-- where 
-- ;

-- select memberNo, memberNam from member;

-- select entrantNo, entrantName from entrant where userNo = 10000009;

select u.phoneNo, u.email
from `edupass-auth`.user u
where exists(
    select 1
    from `edupass-service`.user s2
    where (
        s2.email = u.email
        or s2.phoneNo = u.phoneNo
    )
    and s2.adminAuthCode is not null
);