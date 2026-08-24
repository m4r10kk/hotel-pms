#!/bin/bash
sed -i '' '/<tbody>/,/<\/tbody>/c\
                <tbody>\
                  {users.map(u => (\
                    <tr key={u.id}>\
                      <td style={{ padding: '"'"'12px 14px'"'"', fontWeight: '"'"'800'"'"' }}>{u.full_name} <br/><span style={{fontSize:'"'"'10px'"'"', color:'"'"'var(--text-500)'"'"', fontWeight:400}}>{u.email}</span></td>\
                      <td style={{ padding: '"'"'12px 14px'"'"' }}><span className="pill pill-orange">{u.system_role}</span></td>\
                      <td style={{ padding: '"'"'12px 14px'"'"', color: '"'"'var(--text-300)'"'"', fontSize: '"'"'12.5px'"'"' }}>{orgs.find(o => o.id === u.organization_id)?.name}</td>\
                      <td style={{ padding: '"'"'12px 14px'"'"' }}><span className="pill pill-emerald">{u.is_active ? '"'"'Activo'"'"' : '"'"'Inactivo'"'"'}</span></td>\
                    </tr>\
                  ))}\
                  {users.length === 0 && (\
                    <tr><td colSpan={4} style={{ padding: '"'"'12px 14px'"'"', color: '"'"'var(--text-500)'"'"' }}>No hay usuarios</td></tr>\
                  )}\
                </tbody>
' src/app/dashboard/page.tsx
