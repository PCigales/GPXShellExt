# GPXShellExt v1.0.0 (https://github.com/PCigales/GPXShellExt)
# Copyright © 2026 PCigales
# This program is licensed under the GNU GPLv3 copyleft license (see https://www.gnu.org/licenses)

from wic import *
from wic import _IUtil, _COMMeta, _WShUtil, _COM_IShellExtInit, _COM_IShellPropSheetExt, _COM_IShellPropSheetExt_impl, _COM_IInitializePropertyStoreWithStream, _COM_IPropertyStoreCapabilities, _COM_IPropertyStoreDelegating, _COM_IPropertyHandler_impl, _SPSUtil, _COM_IInitializePreviewHandlerWithStream, _COM_IPreviewHandlerWithFrame, _COM_IPreviewHandlerOleWindow, _COM_IPreviewHandlerVisuals, _COM_IPreviewHandler, _COM_IPreviewHandler_impl
import GPXTweaker

SETTINGS = {
  'smooth_range': 10.0,
  'ele_gain_threshold': 10.0,
  'alt_gain_threshold': 5.0,
  'slope_range': 80.0,
  'slope_max': 100.0,
  'map_size': 512,
  'map_margin': 500.0,
  'map_infos': {'alias': 'OSM', 'matrix': range(10, 20, 1), 'factor': 1.0},
  'map_handling': {'local_pattern': r'%ProgramData%\GPXShellExt\cache', 'local_expiration': None, 'local_store': False, 'key': None, 'referer': None, 'user_agent': 'GPXShellExt', 'basic_auth': None, 'extra_headers': None, 'only_local': False},
  # 'map_infos': {'alias': 'OSM', 'factor': 1.5},
  # 'map_handling': {'local_pattern': r'%ProgramData%\GPXShellExt\cache', 'local_expiration': None, 'local_store': False, 'key': None, 'referer': None, 'user_agent': 'GPXShellExt', 'basic_auth': None, 'extra_headers': None, 'only_local': False},
  'map_track_thickness': 3.5,
  'map_track_color_own': True,
  'map_track_color_fallback': (1.0, 0.0, 0.0, 1.0),
  'map_background_gamma_amplitude': 1.0,
  'map_background_gamma_exponent': 1.0,
  'graph_line_thickness': 1.5,
  'graph_line_color': (1.0, 0.0, 0.0, 1.0),
  'graph_font_size': 11.0,
  'graph_font_fallback': 'Segoe UI'
}
if (alias := SETTINGS['map_infos'].get('alias')) is not None and (infos := (GPXTweaker.WebMercatorMap.TSAlias if 'matrix' in SETTINGS['map_infos'] else GPXTweaker.WebMercatorMap.MSAlias)(alias)) is not None:
  for k, v in infos.items():
    SETTINGS['map_infos'].setdefault(k, v)
if (cpath := SETTINGS['map_handling'].get('local_pattern')):
   SETTINGS['map_handling']['local_pattern'] = os.path.abspath(os.path.expandvars(cpath))

FR_STRINGS = {
  'Path': 'Chemin',
  'Track': 'Trace',
  'track': 'trace',
  'Name': 'Nom',
  'trackname': 'nom-trace',
  'Trackname': 'Nom trace',
  'Description': 'Description',
  'trackdescription': 'description-trace',
  'Trackdescription': 'Description trace',
  'Start': 'Début',
  'trackstart': 'début-trace',
  'Trackstart': 'Début trace',
  'End': 'Fin',
  'trackend': 'fin-trace',
  'Trackend': 'Fin trace',
  'Duration': 'Durée',
  'trackduration': 'durée-trace',
  'Trackduration': 'Durée trace',
  'Distance': 'Distance',
  'trackdistance': 'distance-trace',
  'Trackdistance': 'Distance trace',
  'EleGain': 'Dénivelé élé',
  'trackelegain': 'dénivelé-élé-trace',
  'Trackelegain': 'Dénivelé élé trace',
  'AltGain': 'Dénivelé alt',
  'trackaltgain': 'dénivelé-alt-trace',
  'Trackaltgain': 'Dénivelé alt trace',
  'Waypoints': 'Points de cheminement',
  'trackwpts': 'repère-trace | repères-trace',
  'Trackwpts': 'Repères trace',
  'segment': 'segment',
  'point': 'point',
  'h': 'h',
  'mn': 'mn',
  's': 's',
  'km': 'km',
  'm': 'm',
  'Errtitle': 'Action interrompue',
  'Errmsg': 'Une erreur vous empêche d\'appliquer des propriétés au fichier',
  'Error': 'Erreur',
  'Retry': 'Réessayer'
}

EN_STRINGS = {
  'Path': 'Path',
  'Track': 'Track',
  'track': 'track',
  'Name': 'Name',
  'trackname': 'track-name',
  'Trackname': 'Track name',
  'Description': 'Description',
  'trackdescription': 'track-description',
  'Trackdescription': 'Track description',
  'Start': 'Start',
  'trackstart': 'track-start',
  'Trackstart': 'Track start',
  'End': 'End',
  'trackend': 'track-end',
  'Trackend': 'Track end',
  'Duration': 'Duration',
  'trackduration': 'track-duration',
  'Trackduration': 'Track duration',
  'Distance': 'Distance',
  'trackdistance': 'track-distance',
  'Trackdistance': 'Track distance',
  'EleGain': 'Ele gain',
  'trackelegain': 'track-ele-gain',
  'Trackelegain': 'Track ele gain',
  'AltGain': 'Alt gain',
  'trackaltgain': 'track-alt-gain',
  'Trackaltgain': 'Track alt gain',
  'Waypoints': 'Waypoints',
  'trackwpts': 'track-waypoint | track-waypoints',
  'Trackwpts': 'Track waypoints',
  'segment': 'segment',
  'point': 'point',
  'h': 'h',
  'mn': 'mn',
  's': 's',
  'km': 'km',
  'm': 'm',
  'Errtitle': 'Interrupted action',
  'Errmsg': 'An error is keeping you from applying properties to the file',
  'Error': 'Error',
  'Retry': 'Retry'
}

LSTRINGS = EN_STRINGS
try:
  if GPXTweaker.locale.getlocale()[0][:2].lower() == 'fr':
    LSTRINGS = FR_STRINGS
except:
  pass


class _COM_IGPXShellPropSheetExt(_COM_IShellPropSheetExt):
  Title = 'GPX'
  @classmethod
  def GPXTemplate(cls, file, content, readonly):
    nbtrk = 1
    nbvtrk = 0
    trk = 0
    trck = None
    tconts = []
    tnames = []
    tdescs = []
    twpts = None
    tstarts = []
    tends = []
    tdurs = []
    tdists = []
    tegains = []
    tagains = []
    while trk < nbtrk:
      track = GPXTweaker.WGS84PropertiesTrack()
      trck = trck or track
      if not track.LoadGPX(content, trk, trck, 'f', egthreshold=SETTINGS['ele_gain_threshold'], agthreshold=SETTINGS['alt_gain_threshold'], smdrange=SETTINGS['smooth_range'], sldrange=SETTINGS['slope_range'], slmax=SETTINGS['slope_max']):
        if trck.Wpts is None:
          nbtrk = 0
          break
        tconts.append(None)
        tnames.append(None)
        tdescs.append(None)
        tstarts.append(None)
        tends.append(None)
        tdurs.append(None)
        tdists.append(None)
        tegains.append(None)
        tagains.append(None)
      else:
        nbvtrk += 1
        tconts.append(ctypes.create_unicode_buffer('%d %s%s, %d %s%s' %(track.NSegs, LSTRINGS['segment'], ('s' if track.NSegs >= 2 else ''), track.NPts, LSTRINGS['point'], ('s' if track.NPts >= 2 else ''))))
        tnames.append(ctypes.create_unicode_buffer(track.Name))
        tdescs.append(ctypes.create_unicode_buffer(track.Desc))
        tstarts.append(ctypes.create_unicode_buffer('' if track.Start is None else datetime.datetime.fromtimestamp(track.Start).strftime('%x %X')))
        tends.append(ctypes.create_unicode_buffer('' if track.End is None else datetime.datetime.fromtimestamp(track.End).strftime('%x %X')))
        tdurs.append(ctypes.create_unicode_buffer('' if track.Dur is None else '%d%s%02d%s%02.0f%s' % (track.Dur // 3600, LSTRINGS['h'], track.Dur % 3600 // 60, LSTRINGS['mn'], track.Dur % 60, LSTRINGS['s'])))
        tdists.append(ctypes.create_unicode_buffer('' if track.Dist is None else '%s %s' % (('%.2f' % track.Dist_r).rstrip('0').rstrip('.'), LSTRINGS['km'])))
        tegains.append(ctypes.create_unicode_buffer('' if track.EGain is None else '%.0f%s' % (track.EGain_r, LSTRINGS['m'])))
        tagains.append(ctypes.create_unicode_buffer('' if track.AGain is None else '%.0f%s' % (track.AGain_r, LSTRINGS['m'])))
      if nbtrk == 1:
        nbtrk = track.NbGPXTrks
        if track.Wpts:
          twpts = ctypes.create_unicode_buffer('\r\n'.join(track.Wpts))
      trk += 1
    del trck.Track
    tr = '%s %%-%dd' % (LSTRINGS['Track'], len(str(max(0, nbtrk - 1))))
    ts = tuple(map(ctypes.create_unicode_buffer, ('GPX', 'MS Shell Dlg', ('%s:' % LSTRINGS['Path']), file, tr % 0, ('%s:' % LSTRINGS['Name']), ('%s:' % LSTRINGS['Description']), ('%s:' % LSTRINGS['Start']), ('%s:' % LSTRINGS['End']), ('%s:' % LSTRINGS['Duration']), ('%s:' % LSTRINGS['Distance']), ('%s:' % LSTRINGS['EleGain']), ('%s:' % LSTRINGS['AltGain']), ('%s:' % LSTRINGS['Waypoints']))))
    b = ctypes.create_string_buffer(cls._header_size(ts[0], ts[1]) + cls._text_item_size(ts[2]) + cls._text_item_size(ts[3]) + (nbtrk + 1) * cls._text_item_size() + nbtrk * cls._text_item_size(ts[4]) + nbvtrk * sum(cls._text_item_size(ts[i]) for i in range(5, 13)) + sum(cls._text_item_size(t) for ts in (tconts, tnames, tdescs, tstarts, tends, tdurs, tdists, tegains, tagains) for t in ts if t is not None) + (cls._text_item_size(ts[13]) + cls._text_item_size(twpts) if twpts is not None else 0))
    dt, o = cls._header(b, 'Child | Visible | Caption | VScroll | ModalFrame | SetFont', 0, 2 * nbtrk + 17 * nbvtrk + (5 if twpts else 3), 0, 0, 150, 250, ts[0], (9, ts[1]))
    dit, o = cls._text_item(b, o, 'Child | Visible | TabStop', 0, 5, 2, 30, 10, 0xffff, 0x0082, ts[2])
    dit, o = cls._text_item(b, o, 'Child | Visible | EditAutoHScroll | EditReadOnly', 0, 40, 2, 94, 10, 10, 0x0081, ts[3])
    y = 17
    for i in range(nbtrk):
      dit, o = cls._text_item(b, o, 'Child | Visible | StaticEtchedHorz', 0, 0, y, 150, 1, 0xffff, 0x0082)
      dit, o = cls._text_item(b, o, 'Child | Visible', 0, 5, (y := y + 3), 45, 10, 0xffff, 0x0082, ctypes.create_unicode_buffer(tr % i))
      if tconts[i] is not None:
        dit, o = cls._text_item(b, o, 'Child | Visible | EditRight | EditAutoHScroll | EditReadOnly', 0, 60, y, 74, 10, 10 * (i + 1) + 1, 0x0081, tconts[i])
        dit, o = cls._text_item(b, o, 'Child | Visible', 0, 10, (y := y + 10), 45, 10, 0xffff, 0x0082, ts[5])
        dit, o = cls._text_item(b, o, 'Child | Visible | EditAutoHScroll | TabStop%s' % (' | EditReadOnly' if readonly else ''), 0, 60, y, 74, 10, 10 * (i + 1) + 2, 0x0081, tnames[i])
        dit, o = cls._text_item(b, o, 'Child | Visible', 0, 10, (y := y + 10), 45, 10, 0xffff, 0x0082, ts[7])
        dit, o = cls._text_item(b, o, 'Child | Visible | TabStop | EditReadOnly', 0, 60, y, 10, 10, 10 * (i + 1) + 4, 0x0081, tstarts[i])
        dit, o = cls._text_item(b, o, 'Child | Visible', 0, 74, y, 45, 10, 0xffff, 0x0082, ts[8])
        dit, o = cls._text_item(b, o, 'Child | Visible | TabStop | EditReadOnly', 0, 124, y, 10, 10, 10 * (i + 1) + 5, 0x0081, tends[i])
        dit, o = cls._text_item(b, o, 'Child | Visible', 0, 10, (y := y + 10), 45, 10, 0xffff, 0x0082, ts[9])
        dit, o = cls._text_item(b, o, 'Child | Visible | TabStop | EditReadOnly', 0, 60, y, 10, 10, 10 * (i + 1) + 6, 0x0081, tdurs[i])
        dit, o = cls._text_item(b, o, 'Child | Visible', 0, 74, y, 45, 10, 0xffff, 0x0082, ts[10])
        dit, o = cls._text_item(b, o, 'Child | Visible | TabStop | EditReadOnly', 0, 124, y, 10, 10, 10 * (i + 1) + 7, 0x0081, tdists[i])
        dit, o = cls._text_item(b, o, 'Child | Visible', 0, 10, (y := y + 10), 45, 10, 0xffff, 0x0082, ts[11])
        dit, o = cls._text_item(b, o, 'Child | Visible | TabStop | EditReadOnly', 0, 60, y, 10, 10, 10 * (i + 1) + 8, 0x0081, tegains[i])
        dit, o = cls._text_item(b, o, 'Child | Visible', 0, 74, y, 45, 10, 0xffff, 0x0082, ts[12])
        dit, o = cls._text_item(b, o, 'Child | Visible | EditAutoHScroll | TabStop | EditReadOnly', 0, 124, y, 10, 10, 10 * (i + 1) + 9, 0x0081, tagains[i])
        dit, o = cls._text_item(b, o, 'Child | Visible', 0, 10, (y := y + 10), 45, 10, 0xffff, 0x0082, ts[6])
        dit, o = cls._text_item(b, o, 'Child | Visible | VScroll | EditAutoVScroll | EditWantReturn | EditMultiline | TabStop%s' % (' | EditReadOnly' if readonly else ''), 0, 60, y, 74, 32, 10 * (i + 1) + 3, 0x0081, tdescs[i])
        y += 22
      y += 12
    dit, o = cls._text_item(b, o, 'Child | Visible | StaticEtchedHorz', 0, 0, y, 150, 1, 0xffff, 0x0082)
    if twpts is not None:
      dit, o = cls._text_item(b, o, 'Child | Visible', 0, 5, (y := y + 3), 75, 10, 0xffff, 0x0082, ts[13])
      dit, o = cls._text_item(b, o, 'Child | Visible | VScroll | EditAutoVScroll | EditMultiline | EditReadOnly', 0, 10, (y := y + 10), 124, 32, 10 * (i + 3), 0x0081, twpts)
    return DLGPTEMPLATE(dt)
  @classmethod
  def _DlgProc(cls, hWnd, uMsg, wParam, lParam):
    r = 0
    if uMsg == 1024:
      d = DLGHWND(hWnd)
      if (rd0 := d.MapDialogRect((0, 0, 150, 250))) is not None and (r := _SPSUtil.GetTabDisplayRect(d)) is not None and d.Move((r.left, r.top, r.right - r.left, r.bottom - r.top), False) and (rd := d.Rect) is not None:
        wg = rd.right - rd.left + rd0.left - rd0.right
        c = None
        while (c := d.FindChildWindow(c, 'Static', '')):
          if (r := c.Rect) is not None:
            c.Move((0, r.top - rd.top, r.right - r.left + wg, r.bottom - r.top), False)
        for n in (('%s:' % LSTRINGS['End']), ('%s:' % LSTRINGS['Distance']), ('%s:' % LSTRINGS['AltGain'])):
          c = None
          while (c := d.FindChildWindow(c, 'Static', n)):
            if (r := c.Rect) is not None:
              c.Move((r.left - rd.left + wg // 2, r.top - rd.top, r.right - r.left, r.bottom - r.top), False)
        c = None
        while (c := d.FindChildWindow(c, 'Edit')):
          if (i := d.GetItemID(c)) and (r := c.Rect) is not None:
            i %= 10
            if i <= 3:
              c.Move((r.left - rd.left, r.top - rd.top, r.right - r.left + wg, r.bottom - r.top), False)
            elif i % 2:
              c.Move((r.left - rd.left + wg // 2, r.top - rd.top, r.right - r.left + wg // 2, r.bottom - r.top), False)
            else:
              c.Move((r.left - rd.left, r.top - rd.top, r.right - r.left + wg // 2, r.bottom - r.top), False)
        d.Update()
      r = 1
    elif uMsg == 78:
      if DLGNMHDR.from_address(lParam).code == 4294967094:
        d = DLGHWND(hWnd)
        trck = None
        track = None
        pstream = None
        pdeststream = None
        file = d.GetItemText(10)
        r = 0x80004005
        i = 1
        while (cn := d.GetItem(i * 10 + 2)) and (cd := d.GetItem(i * 10 + 3)):
          if d.GetItemModify(cn) or d.GetItemModify(cd):
            if (vn := d.GetItemText(cn)) is None or (vd := d.GetItemText(cd)) is None:
              break
            track = GPXTweaker.WGS84PropertiesTrack()
            if trck is None:
              if not file or not (pstream := PCOMSTREAM.CreateOnFile(file, 0x12)) or (content := pstream.GetContent()) is None or not (pdeststream := pstream.GetDestinationStream()):
                r = 0x80030005
                break
              trck = track
            if not track.LoadGPX(content, i - 1, trck, 'u') or not track.UpdateGPX(vn, vd):
              break
          i += 1
        else:
          if track is None:
            r = 0
          else:
            if (content := track.SaveGPX()) is not None and pdeststream.Write(content) is not None and not ((r := pdeststream.Commit()) & 0x80000000):
              r = pstream.Commit()
        if track is not None:
          del track.Track
        if pdeststream:
          pdeststream.Release()
        if pstream:
          pstream.Release()
        if r & 0x80000000:
          if hasattr(DialogWindow, 'TaskDialogIndirect'):
            b = wintypes.INT()
            DialogWindow.TaskDialogIndirect((d.Parent, Window.ModuleHandle, 'PositionRelativeToWindow', 'Yes | No', LSTRINGS['Errtitle'], 0,'', '%s.\r\n\r\n%s: %s\r\n\r\n%s %s\r\n\r\n%s ?' % (LSTRINGS['Errmsg'], LSTRINGS['Path'], file, LSTRINGS['Error'], str(WError(r))[1:-1], LSTRINGS['Retry']), 0, None, 'Retry', 0, None, 0), b, None, None)
            b = b.value
          else:
            b = DialogWindow.MessageBox(d, '%s.\r\n\r\n%s: %s\r\n\r\n%s %s\r\n\r\n%s ?' % (LSTRINGS['Errmsg'], LSTRINGS['Path'], file, LSTRINGS['Error'], str(WError(r))[1:-1], LSTRINGS['Retry']), LSTRINGS['Errtitle'], 0x10004)
          if b == 7:
            d.ReturnValue = 0
          else:
            d.ReturnValue = 1
        else:
          d.ReturnValue = 0
        r = 1
    return super()._DlgProc(hWnd, uMsg, wParam, lParam) or r
  @classmethod
  def _CallbackProc(cls, hwnd, uMsg, ppsp):
    if (r := super()._CallbackProc(hwnd, uMsg, ppsp)) and uMsg == 2:
      if not ppsp:
        return 0
      psp = ppsp.contents
      with cls[psp.lParam] as self:
        if not self:
          return 0
        if (nelts := self.nelts) <= 1:
          e = 0
        else:
          try:
            e = int(psp.pszTitle.rsplit(' ', 1)[1]) - 1
          except:
            return 0
        trk = nelts - 1 - e
        if e < 0 or e >= nelts or (file := self.pdtobj.GetFileName(trk)) is None or (s := self.pdtobj.GetFileContent(trk)) is None:
          return None
        content = s.GetContent()
        s.Release()
        if content is None:
          return 0
        self.ppsp[e].pResource = psp.pResource = cls.GPXTemplate(file, content, bool((d := self.pdtobj.GetFileDescriptor(trk)) is not None and d['dwFileAttributes'] & 1))
        return 1
    return r

class _COM_IGPXShellPropSheetExt_impl(metaclass=_COMMeta, interfaces=(_COM_IShellExtInit, _COM_IGPXShellPropSheetExt)):
  CLSID = True
  ThreadingModel = _COM_IShellPropSheetExt_impl.ThreadingModel
  Exts = ('.gpx',)
  _destroy = _COM_IShellPropSheetExt_impl._destroy
_COM_IGPXShellPropSheetExt._impl = _COM_IGPXShellPropSheetExt_impl


class _COM_IGPXInitializePropertyStoreWithStream(_COM_IInitializePropertyStoreWithStream):
  pass

class _COM_IGPXPropertyStoreDelegating(_COM_IPropertyStoreDelegating):
  FMTID_GPXSHELLEXT_GPX = GUID.from_name('GPXShellExt.GPX')
  PKEY_GPXSHELLEXT_GPX_PROPGROUP = (FMTID_GPXSHELLEXT_GPX, 100)
  PKEY_GPXSHELLEXT_GPX_NAME = (FMTID_GPXSHELLEXT_GPX, 101)
  PKEY_GPXSHELLEXT_GPX_DESC = (FMTID_GPXSHELLEXT_GPX, 102)
  PKEY_GPXSHELLEXT_GPX_WPTS = (FMTID_GPXSHELLEXT_GPX, 103)
  PKEY_GPXSHELLEXT_GPX_START = (FMTID_GPXSHELLEXT_GPX, 104)
  PKEY_GPXSHELLEXT_GPX_END = (FMTID_GPXSHELLEXT_GPX, 105)
  PKEY_GPXSHELLEXT_GPX_DUR = (FMTID_GPXSHELLEXT_GPX, 106)
  PKEY_GPXSHELLEXT_GPX_DIST = (FMTID_GPXSHELLEXT_GPX, 107)
  PKEY_GPXSHELLEXT_GPX_EGAIN = (FMTID_GPXSHELLEXT_GPX, 108)
  PKEY_GPXSHELLEXT_GPX_AGAIN = (FMTID_GPXSHELLEXT_GPX, 109)
  @classmethod
  def LazyLoad(cls, self, pKey=None):
    if pKey is not None and pKey.contents.fmtid != cls.FMTID_GPXSHELLEXT_GPX:
      return 1
    pcache = self.pcache
    pstream = self.pstream
    pstream.Seek(0, 0)
    if (content := pstream.GetContent()) is None:
      return 0x80030005
    track = None
    m = 's' if pKey is not None and pKey.contents.pid % 100 <= 3 else 'f'
    if not pcache.GetValue(_COM_IGPXPropertyStoreDelegating.PKEY_GPXSHELLEXT_GPX_PROPGROUP):
      track = GPXTweaker.WGS84PropertiesTrack()
      if not track.LoadGPX(content, 0, None, m, egthreshold=SETTINGS['ele_gain_threshold'], agthreshold=SETTINGS['alt_gain_threshold'], smdrange=SETTINGS['smooth_range'], sldrange=SETTINGS['slope_range'], slmax=SETTINGS['slope_max']):
        return 0x80004005
      pcache.SetValueAndState(cls.PKEY_GPXSHELLEXT_GPX_PROPGROUP, ('VT_LPWSTR', '\u200d'), 0)
      pcache.SetValueAndState(cls.PKEY_GPXSHELLEXT_GPX_NAME, ('VT_LPWSTR', track.Name), 0)
      pcache.SetValueAndState(cls.PKEY_GPXSHELLEXT_GPX_DESC, ('VT_LPWSTR', track.Desc), 0)
      pcache.SetValueAndState(cls.PKEY_GPXSHELLEXT_GPX_WPTS, ('VT_VECTOR | VT_LPWSTR', track.Wpts), 0)
    if m == 'f':
      if track is None:
        track = GPXTweaker.WGS84PropertiesTrack()
        if not track.LoadGPX(content, 0, None, m, egthreshold=SETTINGS['ele_gain_threshold'], agthreshold=SETTINGS['alt_gain_threshold'], smdrange=SETTINGS['smooth_range'], sldrange=SETTINGS['slope_range'], slmax=SETTINGS['slope_max']):
          return 0x80004005
      pcache.SetValueAndState(cls.PKEY_GPXSHELLEXT_GPX_START, (('VT_EMPTY', None) if track.Start is None else ('VT_FILETIME', datetime.datetime.fromtimestamp(track.Start, datetime.UTC))), 0)
      pcache.SetValueAndState(cls.PKEY_GPXSHELLEXT_GPX_END, (('VT_EMPTY', None) if track.End is None else ('VT_FILETIME', datetime.datetime.fromtimestamp(track.End, datetime.UTC))), 0)
      pcache.SetValueAndState(cls.PKEY_GPXSHELLEXT_GPX_DUR, (('VT_EMPTY', None) if track.Dur is None else ('VT_UI8', round(track.Dur) * 10000000)), 0)
      pcache.SetValueAndState(cls.PKEY_GPXSHELLEXT_GPX_DIST, (('VT_EMPTY', None) if track.Dist is None else ('VT_R8', track.Dist_r)), 0)
      pcache.SetValueAndState(cls.PKEY_GPXSHELLEXT_GPX_EGAIN, (('VT_EMPTY', None) if track.EGain is None else ('VT_UI4', track.EGain_r)), 0)
      pcache.SetValueAndState(cls.PKEY_GPXSHELLEXT_GPX_AGAIN, (('VT_EMPTY', None) if track.AGain is None else ('VT_UI4', track.AGain_r)), 0)
    if track is not None:
      del track.Track
    return 0 if m == 'f' else 1
  @classmethod
  def Save(cls, self):
    if self.ManualSafeSave:
      pdeststream = yield True
    pcache = self.pcache
    if (v_s_n := pcache.GetValueAndState(cls.PKEY_GPXSHELLEXT_GPX_NAME)) is None or ((v_s_d := pcache.GetValueAndState(cls.PKEY_GPXSHELLEXT_GPX_DESC))) is None:
      return IGetLastError() or 0x80004005
    if (v_s_n[1] != 2 and v_s_d[1] != 2):
      return 1
    pstream = self.pstream
    if pstream.Seek(0, 0) is None or (content := pstream.GetContent()) is None:
      return 0x80030005
    track = GPXTweaker.WGS84PropertiesTrack()
    if not track.LoadGPX(content, 0, None, 'u'):
      return 0x80004005
    if track.UpdateGPX(v_s_n[0], v_s_d[0]) and (content := track.SaveGPX()) is not None:
      if self.ManualSafeSave and pdeststream:
        r = 0x80030005 if pdeststream.Write(content) is None else 0
      else:
        r = 0x80030005 if pstream.SetSize(0) is None or pdeststream.Write(content) is None else 0
      r = IGetLastError() or r
    else:
      r = 0x80004005
    del track.Track
    return r

class _COM_IGPXPropertyStoreCapabilities(_COM_IPropertyStoreCapabilities):
  ReadOnly = {_COM_IGPXPropertyStoreDelegating.PKEY_Search_Contents, _COM_IGPXPropertyStoreDelegating.PKEY_GPXSHELLEXT_GPX_PROPGROUP, _COM_IGPXPropertyStoreDelegating.PKEY_GPXSHELLEXT_GPX_WPTS, _COM_IGPXPropertyStoreDelegating.PKEY_GPXSHELLEXT_GPX_START, _COM_IGPXPropertyStoreDelegating.PKEY_GPXSHELLEXT_GPX_END, _COM_IGPXPropertyStoreDelegating.PKEY_GPXSHELLEXT_GPX_DUR, _COM_IGPXPropertyStoreDelegating.PKEY_GPXSHELLEXT_GPX_DIST, _COM_IGPXPropertyStoreDelegating.PKEY_GPXSHELLEXT_GPX_EGAIN, _COM_IGPXPropertyStoreDelegating.PKEY_GPXSHELLEXT_GPX_AGAIN}
  @classmethod
  def _IsPropertyWritable(cls, pI, pKey):
    with cls[pI] as self:
      if not self or not pKey:
        return 0x80004003
      return 0 if pKey.contents.to_key() not in cls.ReadOnly and self.pcache.GetValue(_COM_IGPXPropertyStoreDelegating.PKEY_GPXSHELLEXT_GPX_PROPGROUP) else 1

class _COM_IGPXPropertyHandler_impl(metaclass=_COMMeta, interfaces=(_COM_IGPXInitializePropertyStoreWithStream, _COM_IGPXPropertyStoreDelegating, _COM_IGPXPropertyStoreCapabilities)):
  CLSID = True
  ThreadingModel = _COM_IPropertyHandler_impl.ThreadingModel
  Exts = ('.gpx',)
  ManualSafeSave = True
  _destroy = _COM_IPropertyHandler_impl._destroy
_COM_IGPXInitializePropertyStoreWithStream._impl = _COM_IGPXPropertyStoreDelegating._impl = _COM_IGPXPropertyStoreCapabilities._impl = _COM_IGPXPropertyHandler_impl


class _COM_IGPXInitializePreviewHandlerWithStream(_COM_IInitializePreviewHandlerWithStream):
  pass

class _COM_IGPXPreviewHandlerWithFrame(_COM_IPreviewHandlerWithFrame):
  pass

class _COM_IGPXPreviewHandlerOleWindow(_COM_IPreviewHandlerOleWindow):
  pass

class _COM_IGPXPreviewHandlerVisuals(_COM_IPreviewHandlerVisuals):
  _vars['ptextformat'] = wintypes.LPVOID
  @classmethod
  def _SetFont(cls, pI, plf):
    with cls[pI] as self:
      if not (self and plf):
        return 0x80004003
      self.font = plf.contents
      PCOM.Release(wintypes.LPVOID(self.ptextformat))
      if (textformat := None if not (parent := self.parent) or (dwfactory := IDWriteFactory()) is None or (dwgdiinterop := dwfactory.GetGdiInterop()) is None else dwgdiinterop.CreateTextFormatFromLOGFONT(self.font, size=SETTINGS['graph_font_size'])) is not None:
        textformat.SetWordWrapping('NoWrap')
      self.ptextformat = _IUtil.Detach(textformat)
      return 0

class _COM_IGPXPreviewHandler(_COM_IPreviewHandler):
  _vars['ptextformat'] = wintypes.LPVOID
  _vars['pd2d1devicecontext'] = wintypes.LPVOID
  _vars['pdxgiswapchain'] = wintypes.LPVOID
  _vars['pd2d1trackcommandlist'] = wintypes.LPVOID
  _vars['pd2d1graphcommandlist'] = wintypes.LPVOID
  _vars['pd2d1mapdevicecontext'] = wintypes.LPVOID
  _vars['pd2d1mapbitmap'] = wintypes.LPVOID
  _vars['mapsize'] = D2D1SIZEF
  _vars['trackscale'] = wintypes.FLOAT
  _vars['graphscale'] = D2D1SIZEF
  _vars['graphxaxispos'] = wintypes.FLOAT
  _vars['pdwgraphlabelslayout'] = wintypes.LPVOID * 4
  _vars['graphlabelsdims'] = D2D1SIZEF * 4
  @classmethod
  def Load(cls, self, pI):
    if self.pd2d1devicecontext:
      PCOM.Release(wintypes.LPVOID(self.pd2d1trackcommandlist))
      self.pd2d1trackcommandlist = None
      PCOM.Release(wintypes.LPVOID(self.pd2d1mapbitmap))
      self.pd2d1mapbitmap = None
      PCOM.Release(wintypes.LPVOID(self.pd2d1graphcommandlist))
      self.pd2d1graphcommandlist = None
      PCOM.Release(wintypes.LPVOID(self.pdxgiswapchain))
      self.pdxgiswapchain = None
      PCOM.Release(wintypes.LPVOID(self.pd2d1devicecontext))
      self.pd2d1devicecontext = None
      self.pd2d1mapdevicecontext = None
      for i in range(4):
        PCOM.Release(wintypes.LPVOID(self.pdwgraphlabelslayout[i]))
        self.pdwgraphlabelslayout[i] = None
    if (d2d1factory := ID2D1Factory('mt')) is None or (d2d1device := d2d1factory.CreateDevice()) is None or (d2d1devicecontext := d2d1device.CreateDeviceContext()) is None or (dxgiswapchain := d2d1devicecontext.CreateSwapChainFromHwnd(hwnd := self.hwnd)) is None:
      return IGetLastError() or 0x80004005
    self.pdxgiswapchain = _IUtil.Detach(dxgiswapchain)
    dpi = hwnd.Dpi
    d2d1devicecontext.SetDpi(dpi, dpi)
    d2d1devicecontext.SetUnitMode('DIPs')
    pstream = self.pstream
    track = None
    pstream.Seek(0, 0)
    if (content := pstream.GetContent()) is None:
      self.pd2d1devicecontext = _IUtil.Detach(d2d1devicecontext)
      return 0x80030005
    track = GPXTweaker.WGS84PreviewTrack()
    if not track.LoadGPX(content, 0, None, smdrange=SETTINGS['smooth_range'], sldrange=SETTINGS['slope_range'], slmax=SETTINGS['slope_max']) or (xwpts := track.XWpts) is None or (ywpts := track.YWpts) is None or (xpts := track.XPts) is None or (ypts := track.YPts) is None or (arws := track.Arws) is None or (ds := track.Ds) is None or (hs := track.Hs) is None:
      self.pd2d1devicecontext = _IUtil.Detach(d2d1devicecontext)
      return 0x80004005
    del track.Track
    if (minx := min((x for xs in (*xpts, xwpts) for x in xs), default=None)) is None:
      self.pd2d1devicecontext = _IUtil.Detach(d2d1devicecontext)
      return 1
    maxx = max((x for xs in (*xpts, xwpts) for x in xs))
    miny = min((y for ys in (*ypts, ywpts) for y in ys))
    maxy = max((y for ys in (*ypts, ywpts) for y in ys))
    margin = SETTINGS['map_margin']
    wmmax = 6378137.0 * math.pi
    minx = max(min(minx - margin, wmmax), -wmmax)
    maxx = max(min(maxx + margin, wmmax), -wmmax)
    miny = max(min(miny - margin, wmmax), -wmmax)
    maxy = max(min(maxy + margin, wmmax), -wmmax)
    bsize = SETTINGS['map_size']
    dx = maxx - minx
    dy = maxy - miny
    r = min(bsize / dx, bsize / dy)
    bwidth = math.ceil(r * dx * dpi / 96.0)
    bheight = math.ceil(r * dy * dpi / 96.0)
    self.mapsize = (bwidth, bheight) if (d2d1mapbitmap := d2d1devicecontext.CreateTargetBitmap(width=bwidth, height=bheight, dpiX=dpi, dpiY=dpi, drawable=True)) is None else d2d1mapbitmap.GetSize()
    self.trackscale = r
    maxd = max(next((sds[-1] for sds in reversed(ds) if sds), 0.0), 1.0)
    minh = min((h for shs in hs for h in shs), default=0.0)
    maxh = max(max((h for shs in hs for h in shs), default=0.0), minh + 1.0)
    dh = maxh - minh
    self.graphscale = maxd, dh
    if (d2d1trackcommandlist := d2d1devicecontext.CreateCommandList()) is not None and (d2d1graphcommandlist := d2d1devicecontext.CreateCommandList()) is not None and (d2d1strokestyle := d2d1devicecontext.CreateStrokeStyle('Round', 'Round', 'Round', 'Round', 1.0, 'Solid', 0.0, 'Fixed')) is not None and (d2d1arstrokestyle := d2d1devicecontext.CreateStrokeStyle('Flat', 'Triangle', 'Flat', 'Flat', 1.0, 'Solid', 0.0, 'Fixed')) is not None and (d2d1trackbrush := d2d1devicecontext.CreateBrush((SETTINGS['map_track_color_own'] and track.Color) or SETTINGS['map_track_color_fallback'])) is not None and (d2d1greybrush := d2d1devicecontext.CreateBrush((0.8, 0.8, 0.8, 1.0))) is not None and (d2d1graphbrush := d2d1devicecontext.CreateBrush(SETTINGS['graph_line_color'])) is not None and (d2d1trackpathgeometry := d2d1devicecontext.CreatePathGeometry()) is not None and (d2d1trackgeometrysink := d2d1trackpathgeometry.Open()) is not None and (d2d1graphpathgeometry := d2d1devicecontext.CreatePathGeometry()) is not None and (d2d1graphgeometrysink := d2d1graphpathgeometry.Open()) is not None:
      d2d1devicecontext.SetTarget(d2d1trackcommandlist)
      d2d1devicecontext.BeginDraw()
      l_t = SETTINGS['map_track_thickness']
      p_t = l_t * 3.5
      ar_t = l_t * 5
      g_t = SETTINGS['graph_line_thickness']
      p0 = None
      for sxpts, sypts, sarws in zip(xpts, ypts, arws):
        if (l := min(len(sxpts), len(sypts))) == 0:
          continue
        points = (D2D1POINT2F * l).from_buffer(GPXTweaker.array.array('f', (e for x, y in zip(sxpts, sypts) for e in (x - minx, maxy - y))))
        if p0 is None:
          p0 = points[0]
        d2d1trackgeometrysink.BeginFigure(points[0])
        d2d1trackgeometrysink.AddLines(points)
        d2d1trackgeometrysink.EndFigure()
        for x, y, tx, ty in sarws:
          d2d1devicecontext.DrawLine(((x := x - minx) - tx, (y := maxy - y) +  ty), (x, y), d2d1trackbrush, ar_t, d2d1arstrokestyle)
      d2d1trackgeometrysink.Close()
      d2d1devicecontext.DrawGeometry(d2d1trackpathgeometry, d2d1trackbrush, l_t, d2d1strokestyle)
      for x, y in zip(xwpts, ywpts):
        d2d1devicecontext.DrawLine(((x := x - minx), (y := maxy - y)), (x, y), d2d1greybrush, p_t, d2d1strokestyle)
        d2d1devicecontext.DrawLine((x, y), (x, y), d2d1trackbrush, p_t * 0.7, d2d1strokestyle)
      if p0 is not None:
        d2d1devicecontext.DrawLine(p0, p0, d2d1greybrush, p_t * 1.3, d2d1strokestyle)
        d2d1devicecontext.DrawLine(p0, p0, d2d1trackbrush, p_t, d2d1strokestyle)
        d2d1devicecontext.DrawLine(p0, p0, d2d1greybrush, p_t * 0.7, d2d1strokestyle)
        d2d1devicecontext.DrawLine(p0, p0, d2d1trackbrush, p_t * 0.3, d2d1strokestyle)
      d2d1devicecontext.EndDraw()
      d2d1devicecontext.SetTarget(d2d1graphcommandlist)
      d2d1devicecontext.BeginDraw()
      self.graphxaxispos = min(max(maxh / dh, 0.0), 1.0)
      for (sds, shs) in zip(ds, hs):
        if (l := min(len(sds), len(shs))) == 0:
          continue
        points = (D2D1POINT2F * l).from_buffer(GPXTweaker.array.array('f', (e for d, h in zip(sds, shs) for e in (d, maxh - h))))
        d2d1graphgeometrysink.BeginFigure(points[0])
        d2d1graphgeometrysink.AddLines(points)
        d2d1graphgeometrysink.EndFigure()
      d2d1graphgeometrysink.Close()
      d2d1devicecontext.DrawGeometry(d2d1graphpathgeometry, d2d1graphbrush, g_t, d2d1strokestyle)
      d2d1devicecontext.EndDraw()
      if (dwfactory := IDWriteFactory()) is not None and (ptextformat := self.ptextformat or _IUtil.Detach(dwfactory.CreateTextFormat(SETTINGS['graph_font_fallback'], size=SETTINGS['graph_font_size']))) and (dwlmindtextlayout := dwfactory.CreateTextLayout('0', ptextformat, 1e9, 1e9)) is not None and (lmindmetrics := dwlmindtextlayout.GetMetrics()) is not None and (dwlmaxdtextlayout := dwfactory.CreateTextLayout('%s %s' % (('%.1f' % (maxd / 1000)).rstrip('0').rstrip('.'), LSTRINGS['km']), ptextformat, 1e9, 1e9)) is not None and (lmaxdmetrics := dwlmaxdtextlayout.GetMetrics()) is not None and (dwlminhtextlayout := dwfactory.CreateTextLayout('%.0f %s' % (minh, LSTRINGS['m']), ptextformat, 1e9, 1e9)) is not None and (lminhmetrics := dwlminhtextlayout.GetMetrics()) is not None and (dwlmaxhtextlayout := dwfactory.CreateTextLayout('%.0f %s' % (maxh, LSTRINGS['m']), ptextformat, 1e9, 1e9)) is not None and (lmaxhmetrics := dwlmaxhtextlayout.GetMetrics()) is not None:
        dwlmindtextlayout.SetTextAlignment('Center')
        dwlmindtextlayout.SetParagraphAlignment('Near')
        dwlmaxdtextlayout.SetTextAlignment('Center')
        dwlmaxdtextlayout.SetParagraphAlignment('Near')
        dwlminhtextlayout.SetTextAlignment('Trailing')
        dwlminhtextlayout.SetParagraphAlignment('Center')
        dwlmaxhtextlayout.SetTextAlignment('Trailing')
        dwlmaxhtextlayout.SetParagraphAlignment('Center')
        margin = max(lmindmetrics['height'], lmaxdmetrics['height'])
        dwlmindtextlayout.SetMaxWidth(lmindmetrics['width'])
        dwlmindtextlayout.SetMaxHeight(margin)
        dwlmaxdtextlayout.SetMaxWidth(lmaxdmetrics['width'])
        dwlmaxdtextlayout.SetMaxHeight(margin)
        margin = max(lminhmetrics['width'], lmaxhmetrics['width'])
        dwlminhtextlayout.SetMaxWidth(margin)
        dwlminhtextlayout.SetMaxHeight(lminhmetrics['height'])
        dwlmaxhtextlayout.SetMaxWidth(margin)
        dwlmaxhtextlayout.SetMaxHeight(lmaxhmetrics['height'])
        self.pdwgraphlabelslayout[:] = (_IUtil.Detach(dwlmindtextlayout), _IUtil.Detach(dwlmaxdtextlayout), _IUtil.Detach(dwlminhtextlayout), _IUtil.Detach(dwlmaxhtextlayout))
        self.graphlabelsdims[:] = ((lmindmetrics['width'], lmindmetrics['height']), (lmaxdmetrics['width'], lmaxdmetrics['height']), (lminhmetrics['width'], lminhmetrics['height']), (lmaxhmetrics['width'], lmaxhmetrics['height']))
    d2d1devicecontext.SetTarget()
    d2d1trackcommandlist.Close()
    d2d1graphcommandlist.Close()
    self.pd2d1trackcommandlist = _IUtil.Detach(d2d1trackcommandlist)
    self.pd2d1graphcommandlist = _IUtil.Detach(d2d1graphcommandlist)
    self.pd2d1devicecontext = _IUtil.Detach(d2d1devicecontext)
    if d2d1mapbitmap is not None and (d2d1mapdevicecontext := d2d1device.CreateDeviceContext()) is not None:
      self.pd2d1mapdevicecontext = d2d1mapdevicecontext.pI
      d2d1mapdevicecontext.SetDpi(dpi, dpi)
      d2d1mapdevicecontext.SetUnitMode('DIPs')
      pd2d1mapdevicecontext = wintypes.LPVOID.from_buffer(self, self.__class__.pd2d1mapdevicecontext.offset)
      vd2d1mapdevicecontext = d2d1mapdevicecontext.pI.value
      def th():
        Initialize()
        famp = SETTINGS['map_background_gamma_amplitude']
        fexp = SETTINGS['map_background_gamma_exponent']
        if (d2d1mapbitmap2 := d2d1mapdevicecontext.CreateTargetBitmap(width=bwidth, height=bheight, dpiX=dpi, dpiY=dpi, drawable=True) if (famp != 1.0 or fexp != 1.0) and (d2d1effect := d2d1mapdevicecontext.CreateEffect('GammaTransfer')) is not None else None) is not None:
          d2d1effect['RedAmplitude'](famp)
          d2d1effect['RedOffset'](1.0 - famp)
          d2d1effect['RedExponent'](fexp)
          d2d1effect['GreenAmplitude'](famp)
          d2d1effect['GreenOffset'](1.0 - famp)
          d2d1effect['GreenExponent'](fexp)
          d2d1effect['BlueAmplitude'](famp)
          d2d1effect['BlueOffset'](1.0 - famp)
          d2d1effect['BlueExponent'](fexp)
        d2d1mapdevicecontext.SetTarget(d2d1mapbitmap2 or d2d1mapbitmap)
        d2d1mapdevicecontext.BeginDraw()
        d2d1mapdevicecontext.SetAntialiasMode('Aliased')
        d2d1mapdevicecontext.Clear((0.0, 0.5, 0.0, 1.0))
        i = 1
        if tmode := (matrix := (infos := {**SETTINGS['map_infos']}).get('matrix')) is not None:
          m = math.log2(GPXTweaker.WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256 * r * infos.get('factor', 1))
          infos['matrix'] = str(next((matrix[i] for i in range(len(matrix) - 1) if abs(m - int(matrix[i])) < abs(int(matrix[i + 1]) - m)), int(matrix[-1])))
        if (imagingfactory := IWICImagingFactory()) is not None and (gen := GPXTweaker.WebMercatorMap().ProvideTiles(infos, None, minx, miny, maxx, maxy, **SETTINGS['map_handling'], max_pending=15, threads=8) if tmode else (None if (bmap := GPXTweaker.WebMercatorMap().ProvideMap(infos, minx, miny, maxx, maxy, bsize * infos.get('factor', 1), bsize * infos.get('factor', 1), **SETTINGS['map_handling'])) is None else ((0, 0, bmap),))) is not None:
          if tmode:
            iscale = infos['scale'] * r
            iwidth = infos['width'] * iscale
            iheight = infos['height'] * iscale
            itopx = (infos['topx'] - minx) * r
            itopy = (maxy - infos['topy']) * r
          else:
            iwidth = dx * r
            iheight = dy * r
            itopx = itopy = 0
          for row, col, tile in gen:
            if pd2d1mapdevicecontext.value != vd2d1mapdevicecontext:
              gen.close()
              break
            if tile is not None and (pstream := PCOMSTREAM.CreateInMemory(tile)):
              if (d2d1tilebitmap := d2d1mapdevicecontext.CreateBitmapFromStream(pstream, imaging_factory=imagingfactory)) is not None:
                if i == 0:
                  d2d1mapdevicecontext.BeginDraw()
                d2d1mapdevicecontext.DrawBitmap(d2d1tilebitmap, (col * iwidth + itopx, row * iheight + itopy, (col + 1) * iwidth + itopx, (row + 1) * iheight + itopy), interpolation_mode='HighQualityCubic')
                if (i := i + 1) == 8:
                  i = 0
                  d2d1mapdevicecontext.EndDraw()
                d2d1tilebitmap.Release()
              pstream.Release()
        if i != 0:
          d2d1mapdevicecontext.EndDraw()
        if d2d1mapbitmap2 is not None:
          d2d1effect.SetInput(0, d2d1mapbitmap2)
          d2d1mapdevicecontext.SetTarget(d2d1mapbitmap)
          d2d1mapdevicecontext.BeginDraw()
          d2d1mapdevicecontext.DrawImage(d2d1effect)
          d2d1mapdevicecontext.EndDraw()
          d2d1mapdevicecontext.SetTarget()
          d2d1mapbitmap2.Release()
        with cls[pI] as self:
          if self and self.pd2d1mapdevicecontext == vd2d1mapdevicecontext:
            self.pd2d1mapdevicecontext = None
            self.pd2d1mapbitmap = _IUtil.Detach(d2d1mapbitmap)
            hwnd.InvalidateRect()
            hwnd.Update()
        d2d1mapdevicecontext.Release()
        Uninitialize()
      threading.Thread(target=th).start()
    return 0
  @classmethod
  def _PreviewWnd(cls, hWnd, Msg, wParam, lParam):
    if Msg == 5:
      if (pI := Window.GetUserAttribute(hWnd)):
        with cls[pI] as self:
          if self and self.parent and (d2d1devicecontext := ID2D1DeviceContext(self.pd2d1devicecontext)) is not None and (dxgiswapchain := IDXGISwapChain(self.pdxgiswapchain)) is not None:
            dxgiswapchain.ResizeBuffers()
            _IUtil.Detach(dxgiswapchain)
            dpi = Window.GetDpiForWindow(hWnd)
            d2d1devicecontext.SetDpi(dpi, dpi)
            _IUtil.Detach(d2d1devicecontext)
    elif Msg == 15:
      if (pI := Window.GetUserAttribute(hWnd)):
        Window.ValidateRect(hWnd, None)
        with cls[pI] as self:
          if self and self.parent and (d2d1devicecontext := ID2D1DeviceContext(self.pd2d1devicecontext)) is not None:
            if (pd2d1trackcommandlist := self.pd2d1trackcommandlist) and (dxgiswapchain := IDXGISwapChain(self.pdxgiswapchain)) is not None:
              dpix, dpiy = d2d1devicecontext.GetDpi()
              if (d2d1targetbitmap := d2d1devicecontext.CreateTargetBitmap(dxgiswapchain, dpiX=dpix, dpiY=dpiy)) is not None:
                w, h = d2d1targetbitmap.GetSize()
                d2d1devicecontext.SetTarget(d2d1targetbitmap)
                d2d1devicecontext.BeginDraw()
                if self.backgroundcolor == self.textcolor:
                  self.backgroundcolor = 0xffffffff - self.textcolor
                d2d1devicecontext.Clear((((bgcolor := self.backgroundcolor) & 0xff) / 0xff, (bgcolor & 0xff00) / 0xff00, (bgcolor & 0xff0000) / 0xff0000, 1.0))
                bw, bh = self.mapsize.value
                r = min(w / bw, 0.75 * h / bh)
                d2d1devicecontext.SetAntialiasMode('Aliased')
                d2d1devicecontext.SetTransform(idmx := ID2D1Factory.MakeIdentityMatrix())
                if (pd2d1mapbitmap := self.pd2d1mapbitmap):
                  d2d1devicecontext.DrawBitmap(pd2d1mapbitmap, ((w - r * bw) / 2.0, 0.0, (w + r * bw) / 2.0, r * bh), interpolation_mode='HighQualityCubic')
                else:
                  d2d1devicecontext.PushAxisAlignedClip(((w - r * bw) / 2.0, 0.0, (w + r * bw) / 2.0, r * bh), 'Aliased')
                  d2d1devicecontext.Clear((0.0, 0.5, 0.0, 1.0))
                  d2d1devicecontext.PopAxisAlignedClip()
                d2d1devicecontext.SetAntialiasMode('PerPrimitive')
                d2d1devicecontext.SetTransform(ID2D1Factory.MultiplyMatrix(ID2D1Factory.MakeScaleMatrix((rs := r * self.trackscale), rs, (0.0, 0.0)), ID2D1Factory.MakeTranslationMatrix((w - r * bw) / 2.0, 0.0)))
                d2d1devicecontext.DrawImage(pd2d1trackcommandlist, interpolation_mode='HighQualityCubic')
                d2d1devicecontext.SetTransform(idmx)
                if (pd2d1graphcommandlist := self.pd2d1graphcommandlist) and (d2d1strokestyle := d2d1devicecontext.CreateStrokeStyle('Round', 'Round', 'Round', 'Round', 1.0, 'Solid', 0.0, 'Fixed')) is not None and (d2d1brush := d2d1devicecontext.CreateBrush((((fcolor := self.textcolor) & 0xff) / 0xff, (fcolor & 0xff00) / 0xff00, (fcolor & 0xff0000) / 0xff0000, 1.0))) is not None:
                  ds, hs = self.graphscale.value
                  mleft = mright = mtop = mbottom = 3.0
                  mtop += r * bh
                  xay = mtop + self.graphxaxispos * (h - mtop - mbottom)
                  if all(self.pdwgraphlabelslayout):
                    pdwlmindtextlayout, pdwlmaxdtextlayout, pdwlminhtextlayout, pdwlmaxhtextlayout = self.pdwgraphlabelslayout
                    lminddims, lmaxddims, lminhdims, lmaxhdims = self.graphlabelsdims
                    mtop += lmaxhdims.height / 2.0
                    mbottom += lminhdims.height / 2.0
                    if mtop + mbottom + (lminhdims.height + lmaxhdims.height) / 2.0 < h - 6.0:
                      mleft += max(lminhdims.width, lmaxhdims.width) + lminddims.width / 2.0
                      mright += lmaxddims.width / 2.0
                      if (xay := mtop + self.graphxaxispos * (h - mtop - mbottom)) + max(lminddims.height, lmaxddims.height) + 2.0 >= h - 3:
                        mbottom += max(lminddims.height, lmaxddims.height) + 2.0 - lminhdims.height / 2.0
                        xay = mtop + self.graphxaxispos * (h - mtop - mbottom)
                      d2d1devicecontext.DrawTextLayout((mleft - lminddims.width / 2.0, xay + 2.0), pdwlmindtextlayout, d2d1brush, 'Clip')
                      d2d1devicecontext.DrawTextLayout((w - lmaxddims.width, xay + 2.0), pdwlmaxdtextlayout, d2d1brush, 'Clip')
                      d2d1devicecontext.DrawTextLayout((0.0, h - mbottom - lminhdims.height / 2.0), pdwlminhtextlayout, d2d1brush, 'Clip')
                      d2d1devicecontext.DrawTextLayout((0.0, mtop - lmaxhdims.height / 2.0), pdwlmaxhtextlayout, d2d1brush, 'Clip')
                    else:
                      mtop = 3.0 + r * bh
                      mbottom = 3.0
                  d2d1devicecontext.DrawLine((mleft, xay), (w - mright, xay), d2d1brush, (a_t := SETTINGS['graph_line_thickness'] / 1.5), d2d1strokestyle)
                  d2d1devicecontext.DrawLine((mleft, h - mbottom), (mleft, mtop), d2d1brush, a_t, d2d1strokestyle)
                  d2d1devicecontext.SetTransform(ID2D1Factory.MultiplyMatrix(ID2D1Factory.MakeScaleMatrix((w - mleft - mright) / ds, (h - mtop - mbottom) / hs, (0.0, 0.0)), ID2D1Factory.MakeTranslationMatrix(mleft, mtop)))
                  d2d1devicecontext.DrawImage(pd2d1graphcommandlist, interpolation_mode='HighQualityCubic')
                d2d1devicecontext.EndDraw()
                d2d1devicecontext.SetTarget()
                d2d1targetbitmap.Release()
                dxgiswapchain.Present()
              _IUtil.Detach(dxgiswapchain)
            _IUtil.Detach(d2d1devicecontext)
        return 0
    return super()._PreviewWnd(hWnd, Msg, wParam, lParam)
  @classmethod
  def _Unload(cls, pI):
    with cls[pI] as self:
      if not self:
        return 0x80004003
      PCOM.Release(wintypes.LPVOID(self.pd2d1trackcommandlist))
      self.pd2d1trackcommandlist = None
      PCOM.Release(wintypes.LPVOID(self.pd2d1mapbitmap))
      self.pd2d1mapbitmap = None
      PCOM.Release(wintypes.LPVOID(self.pd2d1graphcommandlist))
      self.pd2d1graphcommandlist = None
      PCOM.Release(wintypes.LPVOID(self.pdxgiswapchain))
      self.pdxgiswapchain = None
      PCOM.Release(wintypes.LPVOID(self.pd2d1devicecontext))
      self.pd2d1devicecontext = None
      self.pd2d1mapdevicecontext = None
      for i in range(4):
        PCOM.Release(wintypes.LPVOID(self.pdwgraphlabelslayout[i]))
        self.pdwgraphlabelslayout[i] = None
      return super()._Unload(pI)

class _COM_IGPXPreviewHandler_impl(metaclass=_COMMeta, interfaces=(_COM_IGPXInitializePreviewHandlerWithStream, _COM_IGPXPreviewHandlerWithFrame, _COM_IGPXPreviewHandlerOleWindow, _COM_IGPXPreviewHandlerVisuals, _COM_IGPXPreviewHandler)):
  CLSID = True
  ThreadingModel = _COM_IPreviewHandler_impl.ThreadingModel
  Exts = ('.gpx',)
  def _destroy(self):
    _COM_IPreviewHandler_impl._destroy(self)
    PCOM.Release(wintypes.LPVOID(self.pd2d1trackcommandlist))
    self.pd2d1trackcommandlist = None
    PCOM.Release(wintypes.LPVOID(self.pd2d1mapbitmap))
    self.pd2d1mapbitmap = None
    PCOM.Release(wintypes.LPVOID(self.pd2d1graphcommandlist))
    self.pd2d1graphcommandlist = None
    PCOM.Release(wintypes.LPVOID(self.pdxgiswapchain))
    self.pdxgiswapchain = None
    PCOM.Release(wintypes.LPVOID(self.pd2d1devicecontext))
    self.pd2d1devicecontext = None
    self.pd2d1mapdevicecontext = None
    PCOM.Release(wintypes.LPVOID(self.ptextformat))
    self.ptextformat = None
    for i in range(4):
      PCOM.Release(wintypes.LPVOID(self.pdwgraphlabelslayout[i]))
      self.pdwgraphlabelslayout[i] = None
_COM_IGPXInitializePreviewHandlerWithStream._impl = _COM_IGPXPreviewHandlerWithFrame._impl = _COM_IGPXPreviewHandlerOleWindow._impl = _COM_IGPXPreviewHandlerVisuals._impl = _COM_IGPXPreviewHandler._impl = _COM_IGPXPreviewHandler_impl


def DllInstall(bInstall, pszCmdLine):
  if (l := len((cmdline := pszCmdLine if isinstance(pszCmdLine, str) else ctypes.wstring_at(pszCmdLine)).split('|'))) != 1:
    return ISetLastError(0x80070057)
  rpath = os.path.dirname(os.path.abspath(cmdline[0]))
  p = os.path.join(rpath, 'GPXShellExt.propdesc')
  Initialize()
  r = True
  if bInstall:
    try:
      if (pdpath := _WShUtil.GetKnownFolderPath('ProgramData')):
        pdpath = os.path.abspath(pdpath).lower()
        if os.path.commonpath((pdpath, rpath)).lower() == pdpath:
          pcpath = os.path.join(rpath, '__pycache__')
          os.makedirs(pcpath, exist_ok=True)
          r = os.system('icacls "%s" /grant *S-1-5-32-545:(OI)(CI)M /inheritance:d > nul' % pcpath) == 0
        else:
          pdpath = None
      if SETTINGS['map_handling'].get('local_store') and (cpath := SETTINGS['map_handling'].get('local_pattern')):
        while '{' in cpath:
          cpath = os.path.dirname(cpath)
        if os.path.commonpath((rpath, os.path.dirname(cpath))).lower() == rpath.lower():
          os.makedirs(cpath, exist_ok=True)
          r &= os.system(('icacls "%s" /grant *S-1-5-32-545:(OI)(CI)M /inheritance:d /setintegritylevel (OI)(CI)L> nul' if pdpath else 'icacls "%s" /inheritance:d /setintegritylevel (OI)(CI)L> nul') % cpath) == 0
    except:
      r = False
    fmtid = _COM_IGPXPropertyStoreDelegating.FMTID_GPXSHELLEXT_GPX
    with open(p, 'wt', encoding='utf-8') as f:
      f.write('''\
<?xml version="1.0" encoding="utf-8"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.microsoft.com/windows/2006/propertydescription" schemaVersion="1.0">
  <propertyDescriptionList publisher="PCigales" product="GPXShellExt">
    <propertyDescription name="GPXShellExt.GPX.PropGroup" formatID="{%s}" propID="100">
      <description>Separator for track 0</description>
      <searchInfo inInvertedIndex="false" isColumn="false"/>
      <typeInfo type="Null" isGroup="true" isInnate="true" isViewable="true"/>
      <labelInfo label="%s"/>
    </propertyDescription>
    <propertyDescription name="GPXShellExt.GPX.Name" formatID="{%s}" propID="101">
      <description>Name of the track 0</description>
      <searchInfo inInvertedIndex="true" isColumn="true" columnIndexType="OnDisk" mnemonics="%s"/>
      <typeInfo type="String" isInnate="false" multipleValues="false" isViewable="true" conditionType="String"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="String">
        <stringFormat formatAs="General"/>
      </displayInfo>
    </propertyDescription>
    <propertyDescription name="GPXShellExt.GPX.Desc" formatID="{%s}" propID="102">
      <description>Description of the track 0</description>
      <searchInfo inInvertedIndex="true" isColumn="true" columnIndexType="OnDisk" mnemonics="%s"/>
      <typeInfo type="String" isInnate="false" multipleValues="false" isViewable="true" conditionType="String"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="String">
        <stringFormat formatAs="General"/>
        <drawControl control="MultiLineText"/>
        <editControl control="MultiLineText"/>
      </displayInfo>
    </propertyDescription>
    <propertyDescription name="GPXShellExt.GPX.Wpts" formatID="{%s}" propID="103">
      <description>Waypoints of the track 0</description>
      <searchInfo inInvertedIndex="true" isColumn="true" columnIndexType="OnDiskVector" mnemonics="%s"/>
      <typeInfo type="String" isInnate="true" multipleValues="true" isViewable="true" conditionType="String"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="String">
        <stringFormat formatAs="General"/>
        <drawControl control="MultiValueText"/>
      </displayInfo>
    </propertyDescription>
    <propertyDescription name="GPXShellExt.GPX.Start" formatID="{%s}" propID="104">
      <description>Start date of the track 0</description>
      <searchInfo inInvertedIndex="false" isColumn="true" columnIndexType="OnDisk" mnemonics="%s"/>
      <typeInfo type="DateTime" isInnate="true" multipleValues="false" isViewable="true" conditionType="DateTime" aggregationType="DateRange"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="DateTime">
        <dateTimeFormat formatAs="General" formatTimeAs="LongTime" formatDateAs="ShortDate"/>
        <drawControl control="StaticText"/>
      </displayInfo>
    </propertyDescription>
    <propertyDescription name="GPXShellExt.GPX.End" formatID="{%s}" propID="105">
      <description>End date of the track 0</description>
      <searchInfo inInvertedIndex="false" isColumn="true" columnIndexType="OnDisk" mnemonics="%s"/>
      <typeInfo type="DateTime" isInnate="true" multipleValues="false" isViewable="true" conditionType="DateTime" aggregationType="DateRange"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="DateTime">
        <dateTimeFormat formatAs="General" formatTimeAs="LongTime" formatDateAs="ShortDate"/>
        <drawControl control="StaticText"/>
      </displayInfo>
    </propertyDescription>
    <propertyDescription name="GPXShellExt.GPX.Dur" formatID="{%s}" propID="106">
      <description>Duration of the track 0</description>
      <searchInfo inInvertedIndex="false" isColumn="true" columnIndexType="OnDisk" mnemonics="%s"/>
      <typeInfo type="UInt64" isInnate="true" multipleValues="false" isViewable="true" conditionType="Number" aggregationType="Sum"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="Number" alignment="Center">
        <numberFormat formatAs="Duration" formatDurationAs="hh:mm:ss"/>
        <drawControl control="StaticText"/>
      </displayInfo>
    </propertyDescription>
    <propertyDescription name="GPXShellExt.GPX.Dist" formatID="{%s}" propID="107">
      <description>Distance of the track 0</description>
      <searchInfo inInvertedIndex="false" isColumn="true" columnIndexType="OnDisk" mnemonics="%s"/>
      <typeInfo type="Double" isInnate="true" multipleValues="false" isViewable="true" conditionType="Number" aggregationType="Sum"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="Number" alignment="Center">
        <numberFormat formatAs="General"/>
        <drawControl control="StaticText"/>
      </displayInfo>
    </propertyDescription>
    <propertyDescription name="GPXShellExt.GPX.EGain" formatID="{%s}" propID="108">
      <description>Elevation gain of the track 0</description>
      <searchInfo inInvertedIndex="false" isColumn="true" columnIndexType="OnDisk" mnemonics="%s"/>
      <typeInfo type="UInt32" isInnate="true" multipleValues="false" isViewable="true" conditionType="Number" aggregationType="Sum"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="Number" alignment="Center">
        <numberFormat formatAs="General"/>
        <drawControl control="StaticText"/>
      </displayInfo>
    </propertyDescription>
    <propertyDescription name="GPXShellExt.GPX.AGain" formatID="{%s}" propID="109">
      <description>Altitude gain of the track 0</description>
      <searchInfo inInvertedIndex="false" isColumn="true" columnIndexType="OnDisk" mnemonics="%s"/>
      <typeInfo type="UInt32" isInnate="true" multipleValues="false" isViewable="true" conditionType="Number" aggregationType="Sum"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="Number" alignment="Center">
        <numberFormat formatAs="General"/>
        <drawControl control="StaticText"/>
      </displayInfo>
    </propertyDescription>
  </propertyDescriptionList>
</schema>''' % (fmtid, LSTRINGS['Track'], fmtid, LSTRINGS['trackname'], LSTRINGS['Trackname'], fmtid, LSTRINGS['trackdescription'], LSTRINGS['Trackdescription'], fmtid, LSTRINGS['trackwpts'], LSTRINGS['Trackwpts'], fmtid, LSTRINGS['trackstart'], LSTRINGS['Trackstart'], fmtid, LSTRINGS['trackend'], LSTRINGS['Trackend'], fmtid, LSTRINGS['trackduration'], LSTRINGS['Trackduration'], fmtid, LSTRINGS['trackdistance'], LSTRINGS['Trackdistance'], fmtid, LSTRINGS['trackelegain'], LSTRINGS['Trackelegain'], fmtid, LSTRINGS['trackaltgain'], LSTRINGS['Trackaltgain']))
    r = r and \
      COMRegistration.RegistryAddPropertySchema(p) and \
      COMRegistration.RegistryAddCOMFactory(_COM_IGPXShellPropSheetExt_impl, user=False) and \
      COMRegistration.RegistryAddShellPropSheetHandler(_COM_IGPXShellPropSheetExt_impl, 'GPXShellExt', user=False) and \
      COMRegistration.RegistryAddCOMFactory(_COM_IGPXPropertyHandler_impl, user=False) and \
      COMRegistration.RegistryAddPropertyHandler(_COM_IGPXPropertyHandler_impl, full_details='+GPXShellExt.GPX.PropGroup;GPXShellExt.GPX.Name;GPXShellExt.GPX.Start;GPXShellExt.GPX.End;GPXShellExt.GPX.Dur;GPXShellExt.GPX.Dist;GPXShellExt.GPX.EGain;GPXShellExt.GPX.AGain;GPXShellExt.GPX.Desc;GPXShellExt.GPX.Wpts', preview_details='+GPXShellExt.GPX.Name;*GPXShellExt.GPX.Start;*GPXShellExt.GPX.End;*GPXShellExt.GPX.Dur;*GPXShellExt.GPX.Dist;*GPXShellExt.GPX.EGain;*GPXShellExt.GPX.AGain;GPXShellExt.GPX.Desc;*GPXShellExt.GPX.Wpts', content_layout='alpha', content_mode_browse='~GPXShellExt.GPX.Name;GPXShellExt.GPX.Dur;~System.ItemNameDisplay;~GPXShellExt.GPX.Desc;GPXShellExt.GPX.Dist;GPXShellExt.GPX.EGain;GPXShellExt.GPX.AGain', content_mode_search='~GPXShellExt.GPX.Name;GPXShellExt.GPX.Dur;~System.ItemPathDisplay;~GPXShellExt.GPX.Desc;GPXShellExt.GPX.Dist;GPXShellExt.GPX.EGain;GPXShellExt.GPX.AGain', user=False) and \
      COMRegistration.RegistryAddCOMFactory(_COM_IGPXPreviewHandler_impl, user=False) and \
      COMRegistration.RegistryAddPreviewHandler(_COM_IGPXPreviewHandler_impl, user=False)
  else:
    r = \
      COMRegistration.RegistryRemovePreviewHandler(_COM_IGPXPreviewHandler_impl, user=False) and \
      COMRegistration.RegistryRemoveCOMFactory(_COM_IGPXPreviewHandler_impl, user=False) and \
      COMRegistration.RegistryRemovePropertyHandler(_COM_IGPXPropertyHandler_impl, user=False) and \
      COMRegistration.RegistryRemoveCOMFactory(_COM_IGPXPropertyHandler_impl, user=False) and \
      COMRegistration.RegistryRemoveShellPropSheetHandler(_COM_IGPXShellPropSheetExt_impl, 'GPXShellExt', user=False) and \
      COMRegistration.RegistryRemoveCOMFactory(_COM_IGPXShellPropSheetExt_impl, user=False) and \
      COMRegistration.RegistryRemovePropertySchema(p)
  Uninitialize()
  return ISetLastError(0 if r else IGetLastError() or 0x8000ffff)


if __name__ == '__main__' and len(sys.argv) >= 2:
  if COMRegistration.IsAdmin() is False:
    if (r := COMRegistration.RunAsAdmin()) is None:
      r = 0x8000ffff
    print(WError(r))
    sys.exit(r)
  if (a := sys.argv[1].lstrip('-/').lower()) == 'register':
    r = DllInstall(True, os.path.dirname(os.path.abspath(__file__)))
  elif a == 'unregister':
    r = DllInstall(False, os.path.dirname(os.path.abspath(__file__)))
  else:
    r = 0x80070057
  print(WError(r))
  sys.exit(r)