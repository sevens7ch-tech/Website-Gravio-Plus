# © 2026 Christian Haake. Einmalige Umbenennung der Webseite: Gravio Plus -> GravioLOG Public (Adressen bleiben)
import re, sys
def rename(s):
    keep = []
    def protect(p):
        nonlocal s
        s = re.sub(p, lambda m: (keep.append(m.group(0)), f'\x00K{len(keep)-1}\x00')[1], s)
    protect(r'Website-Gravio-Plus'); protect(r'Gravio-Updates'); protect(r'Gravio-Public-Dispo'); protect(r'/Gravio\b')
    for a, b in [('Gravio-Plus-Dispo-Handbuch', 'GravioLOG-Public-Dispo-Handbuch'), ('Gravio-Plus-Handbuch', 'GravioLOG-Public-Handbuch'),
                 ('Gravio-Plus-App', 'GravioLOG-Public-App'), ('Gravio-Plus-', 'GravioLOG-Public-'), ('Gravio Plus', 'GravioLOG Public')]:
        s = s.replace(a, b)
    s = re.sub(r'(?<![A-Za-z_])Gravio(?![A-Za-z_|-])', 'GravioLOG', s)
    s = re.sub(r'\x00K(\d+)\x00', lambda m: keep[int(m.group(1))], s)
    return s
for p in sys.argv[1:]:
    t = open(p, encoding='utf-8').read(); n = rename(t)
    open(p, 'w', encoding='utf-8').write(n); print(p, t.count('Gravio Plus'), '->', n.count('GravioLOG'))
