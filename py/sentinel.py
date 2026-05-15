import argparse
import datetime
import os
import pathlib
import re
import subprocess
import sys
import tempfile


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            'Run sql/changed_within.sql and write a sentinel file with datasets '
            'changed in the selected time window.'
        )
    )

    parser.add_argument('env', choices=['dev', 'stg', 'prd'], help='Evidence room environment')
    parser.add_argument('--dbuser', required=True, help='Oracle username')
    parser.add_argument('--dbname', required=True, help='Database name (matches TNS entry in tnsnames.ora)')
    parser.add_argument(
        '--dbpassword',
        required=True,
        help='Oracle password.',
    )
    parser.add_argument('--owner', default='CSCL', help='Schema owner for CSCL views')
    parser.add_argument(
        '--within',
        default='year',
        choices=['day', 'week', 'month', 'year'],
        help='Modified-date lookback window',
    )
    parser.add_argument(
        '--evidenceroom-root',
        default=None,
        help='Path to evidenceroom root. Defaults to <repo>/evidenceroom',
    )
    return parser.parse_args()


def escape_sql_literal(value):
    return value.replace("'", "''")


def parse_rows(raw_output):
    rows = []
    for line in raw_output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('PL/SQL procedure successfully completed'):
            continue
        if stripped.startswith('SP2-') or stripped.startswith('ORA-'):
            continue
        match = re.match(r'^([A-Za-z0-9_]+)\s+([0-9]+)$', stripped)
        if match:
            rows.append((match.group(1), int(match.group(2))))
    return rows


def parse_unknown_rows(raw_output):
    names = []
    for line in raw_output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('PL/SQL procedure successfully completed'):
            continue
        if stripped.startswith('SP2-') or stripped.startswith('ORA-'):
            continue
        if re.match(r'^[A-Za-z0-9_]+$', stripped):
            names.append(stripped)
    return names


def _run_sqlplus(connect_target, command_block):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False, encoding='utf-8') as tf:
        tf.write('\n'.join(command_block) + '\n')
        temp_sql_path = tf.name

    try:
        proc = subprocess.run(
            ['sqlplus', '-s', '-L', connect_target, f'@{temp_sql_path}'],
            capture_output=True,
            text=True,
            check=False,
        )
    finally:
        if os.path.exists(temp_sql_path):
            os.remove(temp_sql_path)

    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise RuntimeError(f'SQL*Plus failed with exit code {proc.returncode}: {detail}')

    if 'ORA-' in proc.stdout or 'SP2-' in proc.stdout:
        raise RuntimeError(proc.stdout.strip())

    return proc.stdout


def run_changed_within_sqlplus(args, sql_file_path):
    connect_target = f"{args.dbuser}/{args.dbpassword}@{args.dbname}"
    command_block = [
        'set heading off',
        'set pagesize 0',
        'set feedback off',
        'set verify off',
        'set echo off',
        'set trimspool on',
        'set linesize 32767',
        'set serveroutput off',
        'var p_checkwithinlast varchar2(32)',
        'var p_csclowner varchar2(32)',
        'var p_result_cursor refcursor',
        f"exec :p_checkwithinlast := '{escape_sql_literal(args.within)}';",
        f"exec :p_csclowner := '{escape_sql_literal(args.owner.upper())}';",
        f"@{sql_file_path}",
        'print p_result_cursor',
        'exit',
    ]
    return parse_rows(_run_sqlplus(connect_target, command_block))


def run_unversioned_sqlplus(args, sql_file_path):
    connect_target = f"{args.dbuser}/{args.dbpassword}@{args.dbname}"
    command_block = [
        'set heading off',
        'set pagesize 0',
        'set feedback off',
        'set verify off',
        'set echo off',
        'set trimspool on',
        'set linesize 32767',
        'set serveroutput off',
        'var p_csclowner varchar2(32)',
        'var p_result_cursor refcursor',
        f"exec :p_csclowner := '{escape_sql_literal(args.owner.upper())}';",
        f"@{sql_file_path}",
        'print p_result_cursor',
        'exit',
    ]
    return parse_unknown_rows(_run_sqlplus(connect_target, command_block))


def write_sentinel_file(evidence_root, env, rows, unknown_datasets, within):
    target_dir = os.path.join(evidence_root, env)
    os.makedirs(target_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    out_path = os.path.join(target_dir, f'sentinel-{timestamp}.log')

    with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
        if rows:
            f.write(f"WARNING: The following datasets changed within the last '{within}'.\n")
            for dataset, record_count in rows:
                f.write(f'{dataset}: {record_count}\n')
        else:
            f.write('No datasets changed in the selected window.\n')

        if unknown_datasets:
            f.write('\n')
            for dataset in unknown_datasets:
                f.write(f'{dataset}: unknown\n')

    return out_path


def main():
    args = parse_args()

    repo_root = pathlib.Path(__file__).resolve().parents[1]
    evidence_root = args.evidenceroom_root or os.path.join(repo_root, 'evidenceroom')
    sql_file_path = os.path.join(str(repo_root), 'sql', 'changed_within.sql')
    unversioned_sql_path = os.path.join(str(repo_root), 'sql', 'unversioned_datasets.sql')

    rows = run_changed_within_sqlplus(args, sql_file_path)
    unknown_datasets = run_unversioned_sqlplus(args, unversioned_sql_path)
    out_path = write_sentinel_file(evidence_root, args.env, rows, unknown_datasets, args.within)

    print(out_path)
    sys.exit(0)


if __name__ == '__main__':
    main()
