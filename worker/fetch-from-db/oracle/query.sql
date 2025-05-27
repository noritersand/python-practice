-- select
--     mem_id
-- from WEB_USR_ACCT
-- where DEL_DTTM is null
-- and (ACCT_BLOFF_YN is null or ACCT_BLOFF_YN = 'N')
-- and (WTDRL_YN is null or WTDRL_YN = 'N')
-- and '19700101000000' <= CRE_DTTM and CRE_DTTM < '20230101000000'
-- order by CRE_DTTM desc
select mem_id
from member