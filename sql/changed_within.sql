declare

    p_checkwithinlast varchar2(32) := nvl(lower(:p_checkwithinlast), 'year');
    p_csclowner       varchar2(32) := nvl(upper(:p_csclowner), 'CSCL');
    p_since_expr      varchar2(128);
    psql              clob;

begin

    p_since_expr := case p_checkwithinlast
        when 'day'   then 'SYSTIMESTAMP - INTERVAL ''1'' DAY'
        when 'week'  then 'SYSTIMESTAMP - INTERVAL ''7'' DAY'
        when 'month' then 'ADD_MONTHS(SYSTIMESTAMP, -1)'
        when 'year'  then 'ADD_MONTHS(SYSTIMESTAMP, -12)'
        else null
    end;

    if p_since_expr is null then
        raise_application_error(-20001, 'p_checkwithinlast must be one of day, week, month, year');
    end if;

    select xmlcast(
               xmlagg(
                   xmlelement(
                       e,
                       'select '''
                       || replace(a.view_name, '_EVW', '')
                       || ''' as dataset, count(*) as record_count from '
                       || dbms_assert.simple_sql_name(a.owner)
                       || '.'
                       || dbms_assert.simple_sql_name(a.view_name)
                       || ' where modified_date >= '
                       || p_since_expr
                       || ' having count(*) > 0 union all '
                   )
                   order by a.view_name
               ) as clob
           )
      into psql
      from all_views a
     where a.owner = p_csclowner
       and a.view_name like '%\_EVW' escape '\';

    if psql is null then
        open :p_result_cursor for
            select cast(null as varchar2(128)) as dataset
                 , cast(null as number) as record_count
              from dual
             where 1 = 0;
    else
        psql := regexp_replace(psql, ' union all $', '');
        open :p_result_cursor for psql;
    end if;
end;
/