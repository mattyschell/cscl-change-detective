declare

    p_csclowner varchar2(32) := nvl(upper(:p_csclowner), 'CSCL');

begin

    open :p_result_cursor for
        select table_name
          from sde.table_registry
         where owner = p_csclowner
           and imv_view_name is null
           and table_name not like '%\_H' escape '\'
           and rowid_column = 'OBJECTID'
           and table_name not like 'T_1_%'
           and table_name not like '%JOB%'
         order by 1;

end;
/
