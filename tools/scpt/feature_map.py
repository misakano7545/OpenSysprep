#!/usr/bin/env python3
"""功能级映射：模块 × 功能关键词矩阵 + 主程序流程标记提取。

输出:
  work/analysis/feature_matrix.md
  work/analysis/main_flow.txt
"""
import pathlib
import re

BASE = pathlib.Path('/root/dev/OpenSysprep')
ENG = BASE / 'work/engines'
AN = BASE / 'work/analysis'
MEX = pathlib.Path('/root/dev/scpt-analysis/01-unpacked/Scpt.unpacked.exe')

FEATURES = {
    '封装流程': ['sysprep', 'generalize', 'oobe', 'unattend', '封装', 'panther', 'setupact'],
    '部署组件': ['sctasks', 'scdeploy', 'scdata', 'deploy', '部署'],
    '任务计划': ['runonce', 'schtasks', 'task scheduler', '计划任务', 'setupcomplete', 'firstlogon'],
    '分辨率': ['resolution', '分辨率', 'videomode', 'refreshrate', 'displayfrequency'],
    '任务栏固定': ['taskbar', '任务栏', 'pintotaskbar', 'quick launch'],
    'OEM': ['oem', 'scoem', '品牌', 'wallpaper', 'logo'],
    'SRS驱动': ['srs', 'driverpack', '磁盘控制器', 'driverstore', 'pnputil', '驱动的'],
    '系统优化': ['优化', 'optimize', 'prefetch', 'superfetch', 'cleanjunk', '服务优化'],
    '默认用户': ['forensit', 'defprof', 'ntuser', 'scruntemp', 'default user'],
    '浏览器篡改': ['newtabx', 'sejai', 'hao_pg', 'homepage', 'homepages', 'setedge',
                   'prefs_enclave', 'secure preferences', 'blbeacon'],
    '浏览器(其他)': ['internet explorer', 'chromium', 'user data', 'startup_urls'],
    '网络设置': ['netsh', 'ipconfig', 'dns', '网络设置'],
    '激活': ['slmgr', '激活', 'kms'],
    '清理': ['cleanjunk', '清理', '清空', '临时文件'],
    '压缩解压': ['7-zip', '7z.exe', 'igor pavlov'],
    '权限ACL': ['setacl', 'aces', '权限'],
    '引导': ['ntldr', 'bcd', '引导'],
    '虚拟机': ['vmware', 'virtualbox', 'vmrun', '虚拟机'],
    '进度界面': ['进度条', 'progressbar', 'aero', '皮肤', 'skin'],
    '文件注入': ['copyfiles', 'copysys', 'system32', 'windows\\system32'],
    '解压释放': ['解压', 'extract', 'unzip', 'pe_extract'],
}

def hits(b, kws):
    low = b.lower()
    n = 0
    for k in kws:
        ka = k.lower().encode('latin1', 'ignore')
        ku = k.lower().encode('utf-16-le', 'ignore')
        if ka:
            n += low.count(ka)
        if ku and ku != ka:
            n += low.count(ku)
    return n

def main():
    lines = ['# 模块 × 功能关键词矩阵（原始扫描输出）', '',
             '命中数为 0 的功能已省略。', '',
             '| 模块 | 功能命中 |', '|---|---|']
    files = [f for f in sorted(ENG.iterdir()) if f.is_file()
             and not f.name.endswith('.unp')
             and f.name not in ('funn_unpacked.exe', 'funnkrx64_unpacked.exe')]
    for f in files:
        b = f.read_bytes()
        res = [(k, hits(b, v)) for k, v in FEATURES.items()]
        res = [(k, n) for k, n in res if n]
        res.sort(key=lambda x: -x[1])
        cell = ', '.join(f'{k}×{n}' for k, n in res) or '(无命中)'
        lines.append(f'| {f.name} | {cell} |')
        print(f'{f.name:16s} {cell[:120]}')

    # 主程序流程标记
    flow = ['# 主程序流程标记（原始提取）', '']
    try:
        mb = MEX.read_bytes()
        pat_u = rb'\[\x00(?:[A-Za-z0-9_.]\x00){3,60}\]\x00'
        pat_a = rb'\[(?:[A-Za-z][A-Za-z0-9_.]{3,60})\]'
        marks = {}
        for m in re.finditer(pat_u, mb):
            s = m.group().decode('utf-16-le', 'ignore').strip('[]')
            if '.' in s:
                marks[s] = marks.get(s, 0) + 1
        for m in re.finditer(pat_a, mb):
            s = m.group().decode('latin1').strip('[]')
            if '.' in s and s[0].isupper():
                marks[s] = marks.get(s, 0) + 1
        top = sorted(marks.items(), key=lambda x: (-x[1], x[0]))
        flow.append(f'共 {len(top)} 个标记\n')
        for s, c in top[:120]:
            flow.append(f'  [{c:5d}] [{s}]')
        print(f'\n主程序标记 {len(top)} 个')
        for s, c in top[:25]:
            print(f'  [{c:5d}] [{s}]')
    except Exception as e:
        flow.append(f'提取失败: {e}')
        print('主程序提取失败:', e)

    (AN / 'feature_matrix.md').write_text('\n'.join(lines), encoding='utf-8')
    (AN / 'main_flow.txt').write_text('\n'.join(flow), encoding='utf-8')
    print(f'\n输出: {AN/"feature_matrix.md"} / main_flow.txt')

if __name__ == '__main__':
    main()
