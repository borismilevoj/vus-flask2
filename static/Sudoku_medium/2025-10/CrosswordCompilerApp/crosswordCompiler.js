// Crosssword Compiler applet code v11.39 (www.crossword-compiler.com); copyright Antony Lewis 2025, WordWeb Software
!(function (t) {
  function e(e, i) {
    let n,
      o,
      r,
      l = 0,
      d = 0,
      p = i.Size,
      h = 0,
      f = 0,
      g = 0,
      m = 0,
      b = 0,
      C = 0,
      x = 0,
      w = 0,
      v = 0,
      y = 0,
      S = 0,
      T = 0,
      E = 0;
    function I() {
      let t = y.find('svg');
      return t.length
        ? 'data:image/svg+xml,' + encodeURIComponent(t.parent().html())
        : 'data:image/' + y.attr('format') + ';base64,' + y.text();
    }
    function k() {
      return (f || (f = Raphael(b.fillRect(0, 0, p, p, { color: u }).get(0), p, p)), f);
    }
    return {
      x: 0,
      y: 0,
      make: function (L, O, z, P) {
        ((d = this), (l = e.Clues), (v = O), (g = L), (f = 0), (r = P), (E = v['grid-line-color']));
        let A = L.attr('x').split('-'),
          R = L.attr('y').split('-');
        return (
          (y = L.find('background-picture')),
          y.length || (y = null),
          (d.x = parseInt(A[0])),
          (d.y = parseInt(R[0])),
          (n = A.length > 1 ? A[1] - A[0] + 1 : 1),
          (o = R.length > 1 ? R[1] - R[0] + 1 : 1),
          (S = d.x * p),
          (T = d.y * p),
          (m = z),
          (function () {
            ((h = {}),
              t.each(
                {
                  x: 0,
                  y: 0,
                  type: '',
                  solution: '',
                  'solve-status': '',
                  'solve-state': '',
                  hint: '',
                  number: '',
                  'top-right-number': '',
                  'left-bar': '',
                  'top-bar': '',
                  'background-shape': '',
                  'background-shape-color': '',
                  'background-color': '',
                  'foreground-color': '',
                  noclue: '',
                  'clue-font-lines': '',
                },
                function (t, e) {
                  let i = g.attr(t);
                  null != i && (h[t] = i);
                }
              ));
            let e = h.type;
            (null == e && ((e = 'letter'), (h.type = e)),
              (w = 'letter' == e),
              (C = 'block' == e),
              (x = 'clue' == e));
          })(),
          (function () {
            let l,
              a = i.Settings,
              d = C && !v['italian-style'] ? a['block-color'] : a['grid-background-color'];
            ((d = h.hasOwnProperty('background-color') ? h['background-color'] : d),
              y &&
                w &&
                'true' != y.attr('rebus') &&
                ((l = I()),
                t("<img src='" + l + "' aria-hidden='true'/>")
                  .css({
                    height: p - 1 + 'px',
                    width: p - 1 + 'px',
                    position: 'absolute',
                    left: S - p + 1,
                    top: T - p + 1,
                  })
                  .appendTo(r)
                  .addClass('GridPic'),
                (d = u)),
              (b = t(s(p * o, p * n, d, T - p, S - p, e.isWordSearch ? d : E))
                .attr(C || x ? {} : { role: 'gridcell', 'aria-rowspan': o, 'aria-colspan': n })
                .appendTo(r)
                .addClass('GridSquare')
                .addClass(C ? 'Block' : x ? 'ClueSq' : 'Let')),
              C &&
                0 != v['italian-style'] &&
                (b.fillRect(2, 2, p - 5, p - 5, { color: v['block-color'] }),
                r.drawRect(S - p, T - p, p, p, { color: E })),
              C || b.data('background-color', d).data('data', h));
          })(),
          C ||
            (e.Attributes['hide-numbers'] ||
              (function () {
                let t;
                (!C &&
                  h.hasOwnProperty('number') &&
                  ((t = document.createElement('span')),
                  t.setAttribute(
                    'style',
                    'font-family:sans-serif;margin-left:2px;font-weight:normal;font-size:' +
                      i.NumberSize +
                      'px;float:left;color:' +
                      v['number-color']
                  ),
                  (t.innerHTML = h.number),
                  b.append(t)),
                  h['top-right-number'] &&
                    ((t = document.createElement('span')),
                    t.setAttribute(
                      'style',
                      'font-family:sans-serif;margin-right:2px;font-size:' +
                        i.NumberSize +
                        'px;float:right;color:' +
                        v['number-color']
                    ),
                    (t.innerHTML = h['top-right-number']),
                    b.append(t)));
              })(),
            h.hasOwnProperty('top-bar') &&
              'true' == h['top-bar'] &&
              r.fillRect(S - p, T - p - 1, p, 3, { color: E }),
            h.hasOwnProperty('left-bar') &&
              'true' == h['left-bar'] &&
              r.fillRect(S - p - 1, T - p, 3, p, { color: E }),
            (function () {
              if (x) {
                var e,
                  n = [],
                  o = h['clue-font-lines'] || 5,
                  r = Math.round(p / o),
                  a = t('<table><tr><td></td></tr></table>')
                    .css({
                      fontSize: r + 'px',
                      width: 'auto',
                      'min-width': 0,
                      border: 0,
                      'border-spacing': 0,
                    })
                    .appendTo(b);
                for (
                  g.find('clue').each(function (e, i) {
                    var o,
                      r,
                      s = t(i).text().split('\\'),
                      d = t(i).attr('word'),
                      p = '';
                    (t.each(s, function (t, e) {
                      p += 0 != t ? '<br/>' + e.slice(1, e.length) : e;
                    }),
                      (r = t('<li/>')
                        .addClass('ClueCell')
                        .attr({ id: 'LI' + d })
                        .css({
                          'list-style-type': 'none',
                          'text-align': 'center',
                          'border-top': e > 0 ? 'solid 1px ' + E : '0px',
                          'margin-top': '0px',
                          'padding-top': '0px',
                          'line-height': 1,
                          'font-family': 'sans-serif',
                        })
                        .html(null != p ? p : '')
                        .appendTo(a.find('td'))
                        .data('data', i)),
                      h['foreground-color'] && r.css('color', h['foreground-color']),
                      n.push(r),
                      d &&
                        ((o = l.Words[d]),
                        r
                          .data('word', d)
                          .data('wdCoords', o)
                          .data('coordinates', o.x + ',' + o.y)
                          .data('Cells', c(o))));
                  }),
                    e = a.find('td li');
                  a.width() > p - 2 && r > 2;

                )
                  ((r -= 0.5), e.css({ fontSize: r + 'px' }));
                for (; a.height() > p - 3 && r > 2; ) ((r -= 0.5), e.css({ fontSize: r + 'px' }));
                var s,
                  d = p - a.height() - 2;
                if (d > 2 && n.length > 1)
                  for (s = 1; s < n.length; s++)
                    n[s].css({
                      'margin-top': d / (2 * n.length) + 'px',
                      'padding-top': d / (2 * n.length) + 'px',
                    });
                a.css({
                  height: '100%',
                  width: '100%',
                  backgroundColor: y
                    ? 'transparent'
                    : h['background-color'] || i.Settings['clue-background-color'],
                });
              }
            })(),
            (function () {
              let e = p,
                i = p,
                n = i,
                o = e,
                r = m,
                l = parseInt(parseFloat(r.stem) * i),
                a = Math.max(1, parseInt((parseFloat(r['head-width']) / 2) * i)),
                s = Math.max(2, parseInt(parseFloat(r['head-length']) * i)),
                d = parseInt(parseFloat(r['bend-start']) * i),
                c = parseInt(parseFloat(r['bend-end']) * i),
                h = parseInt(parseFloat(r['bend-side-offset']) * i),
                u = Math.min(i / 4, d / 1.4),
                f = function (t, e) {
                  k()
                    .path(
                      'M' +
                        t[0] +
                        ' ' +
                        e[0] +
                        'L' +
                        t[1] +
                        ' ' +
                        e[1] +
                        'L' +
                        t[2] +
                        ' ' +
                        e[2] +
                        'Z'
                    )
                    .attr({ stroke: E, fill: E, 'stroke-width': 1 });
                },
                b = function (t, e) {
                  k()
                    .path(
                      'M' +
                        t[0] +
                        ' ' +
                        e[0] +
                        'L' +
                        t[1] +
                        ' ' +
                        e[1] +
                        (t[2] ? 'L' + t[2] + ' ' + e[2] : '')
                    )
                    .attr({ stroke: E, 'stroke-width': 1 });
                };
              t.each(g.find('arrow'), function (i, r) {
                var p,
                  g,
                  m = t(this),
                  C = m.attr('from'),
                  x = m.attr('to'),
                  w = m.attr('from-fraction') ? parseFloat(m.attr('from-fraction')) : 0.5,
                  v = 'bottom',
                  y = 'top',
                  S = 'left',
                  T = 'right';
                if ('true' == m.attr('continue-word'))
                  return (
                    C == S && x == v
                      ? (b([(p = n - h) - l, p, p], [0 + h, 0 + h, 0 + h + l]),
                        f([p - a, p + a, p], [0 + h + l, 0 + h + l, 0 + h + l + s]))
                      : C == y &&
                        x == T &&
                        (b([(p = 0 + h), p, p + l], [(g = o - h) - l, g, g]),
                        f([p + l, p + l, p + l + s], [g - a, g + a, g])),
                    !1
                  );
                (C == v &&
                  (x == y
                    ? (b([(p = (0 + n) / 2), p], [o, o - l]),
                      f([p - a, p + a, p], [o - l, o - l, o - l - s]))
                    : x == S
                      ? (b([(p = n - h), p, p - c], [o, (g = o - d), g]),
                        f([p - c, p - c, p - c - s], [g - a, g + a, g]))
                      : x == T &&
                        (b([(p = 0 + h), p, p + c], [o, o - d, o - d]),
                        f([p + c, p + c, p + c + s], [o - d - a, o - d + a, o - d]))),
                  C == y &&
                    (x == v
                      ? (b([(p = (0 + n) / 2), p], [0, 0 + l]),
                        f([p - a, p + a, p], [0 + l, 0 + l, 0 + l + s]))
                      : x == S
                        ? (b([(p = n - h), p, p - c], [0, (g = 0 + d), g]),
                          f([p - c, p - c, p - c - s], [g - a, g + a, g]))
                        : x == T &&
                          (b([(p = 0 + h), p, p + c], [0, 0 + d, 0 + d]),
                          f([p + c, p + c, p + c + s], [0 + d - a, 0 + d + a, 0 + d]))),
                  C == S &&
                    (x == T
                      ? ((p = 0),
                        (g = parseInt(0 + e * w)),
                        b([p, p + l], [g, g]),
                        f([p + l, p + l, p + l + s], [g - a, g + a, g]))
                      : x == v
                        ? (b([0, (p = 0 + d), p], [(g = 0 + h), g, g + c]),
                          f([p - a, p + a, p], [g + c, g + c, g + c + s]))
                        : x == y &&
                          (b([0, (p = 0 + d), p], [(g = o - h), g, g - c]),
                          f([p - a, p + a, p], [g - c, g - c, g - c - s]))),
                  C == T &&
                    (x == S
                      ? ((p = n),
                        (g = parseInt((0 + e) * w)),
                        b([p, p - l], [g, g]),
                        f([p - l, p - l, p - l - s], [g - a, g + a, g]))
                      : x == v
                        ? (b([n, (p = n - d), p], [(g = 0 + h), g, g + c]),
                          f([p - a, p + a, p], [g + c, g + c, g + c + s]))
                        : x == y &&
                          (b([n, (p = n - d), p], [(g = o - h), g, g - c]),
                          f([p - a, p + a, p], [g - c, g - c, g - c - s]))),
                  'bottomleft' == C &&
                    ((p = 0 + u),
                    (g = o - u),
                    x == y
                      ? (b([0, p, p], [o, g, g - c]),
                        f([p - a, p + a, p], [g - c, g - c, g - c - s]))
                      : x == T &&
                        (b([0, p, p + c], [o, g, g]),
                        f([p + c, p + c, p + c + s], [g - a, g + a, g]))),
                  'bottomright' == C &&
                    ((p = n - u),
                    (g = o - u),
                    x == y
                      ? (b([n, p, p], [o, g, g - c]),
                        f([p - a, p + a, p], [g - c, g - c, g - c - s]))
                      : x == S &&
                        (b([n, p, p - c], [o, g, g]),
                        f([p - c, p - c, p - c - s], [g - a, g + a, g]))),
                  'topleft' == C &&
                    ((p = 0 + u),
                    (g = 0 + u),
                    x == v
                      ? (b([0, p, p], [0, g, g + c]),
                        f([p - a, p + a, p], [g + c, g + c, g + c + s]))
                      : x == T &&
                        (b([0, p, p + c], [0, g, g]),
                        f([p + c, p + c, p + c + s], [g - a, g + a, g]))),
                  'topright' == C &&
                    ((p = n - u),
                    (g = 0 + u),
                    x == v
                      ? (b([n, p, p], [0, g, g + c]),
                        f([p - a, p + a, p], [g + c, g + c, g + c + s]))
                      : x == S &&
                        (b([n, p, p - c], [0, g, g]),
                        f([p - c, p - c, p - c - s], [g - a, g + a, g]))));
              });
            })(),
            (function () {
              if (!w) return !1;
              var t = i.DomForSolution.clone(),
                n = t.find('span'),
                o = b,
                r = 'true' == h.hint,
                l = e.isCoded,
                a = e.isWordSearch,
                s = h.solution;
              (t.appendTo(o),
                r || a || l || i.Goal++,
                o.data('ObjectLetter', n),
                o.data('WordId', []),
                o.data('WordItem', []),
                o.data('LIS', []),
                l && r && i.CodedHint.push(h),
                (!r && !a) || l
                  ? (!i.CodedLetter.hasOwnProperty(s) && l && ((i.CodedLetter[s] = []), i.Goal++),
                    i.CodedLetter.hasOwnProperty(s) && i.CodedLetter[s].push(b))
                  : (n.css({ color: h['foreground-color'] || i.FontColor }),
                    i.DrawSizedLetter(n, s),
                    n.parent().css({ fontWeight: 'bolder' })),
                h['solve-state'] &&
                  (n.html(h['solve-state']), b.data('UserSolution', Data['solve-state'])),
                (h.solution = s || ''),
                o.data('Use', { solution: h.solution, hint: r }));
            })(),
            (function () {
              function t(t, e, i, n, o, r) {
                let l = Math.PI / 180,
                  a = e + n * Math.cos((90 - o) * l),
                  s = i - n * Math.sin((90 - o) * l),
                  d = e + n * Math.cos((90 - r) * l),
                  c = i - n * Math.sin((90 - r) * l);
                return t.path([
                  ['M', a, s],
                  ['A', n, n, 0, 1, 1, d, c],
                ]);
              }
              if (h['background-shape']) {
                let i,
                  n = p / 2,
                  o = !e.Attributes['hide-numbers'],
                  r = k();
                ((i =
                  o && h.hasOwnProperty('top-right-number')
                    ? t(r, n, n, n - 0.5, 65, 390)
                    : o && h.hasOwnProperty('number')
                      ? t(r, n, n, n - 0.5, -20, 300)
                      : t(r, n, n, n - 0.5, 0, 359)),
                  i.attr({ 'stroke-width': 1, stroke: h['background-shape-color'] || E }));
              }
            })()),
          (function () {
            if (!y) return;
            let e,
              i = y,
              l = n,
              a = o,
              d = I(),
              c = 0,
              f = y.attr('href');
            if (
              (f &&
                f.length &&
                (c = t(
                  '<a href="' +
                    f +
                    '" class="img_href" target="_blank" style="display: inline-block"></a>'
                )),
              C)
            )
              if (1 != l || 1 != a) {
                ((e = r.find('div:last')), (b = e), e.data('data', h));
                let i = t("<img src='" + d + "'/>")
                    .css({
                      zIndex: 2,
                      position: 'absolute',
                      background: 'white',
                      left: S - p + 1,
                      top: T - p + 1,
                      'max-width': 'none',
                    })
                    .width(l * p - 1)
                    .height(a * p - 1),
                  n = t(s(a * p - 1, l * p - 1, c ? 'black' : u, T - p, S - p, 'black')).css({
                    zIndex: 2,
                  });
                (c
                  ? (n.append(c), c.append(i.css({ left: 0, top: 0, cursor: 'pointer' })))
                  : i.appendTo(r),
                  n.appendTo(r));
              } else {
                let e = r.fillRect(S - p + 1, T - p + 1, l * p, a * p, p, { color: u });
                (c && e.wrap(c),
                  t("<img src='" + d + "'  style='position: absolute;left:0' />")
                    .width(l * p - 1)
                    .height(a * p - 1)
                    .appendTo(e));
              }
            else
              x
                ? (b.append(
                    t("<img src='" + d + "'  style='position: absolute;top:0;left:0' />")
                      .width(l * p)
                      .height(a * p)
                  ),
                  b.find('img:last').on('click', function () {
                    t(this).parent().find('li').trigger('click');
                  }))
                : ((b.data('Use').img = !1),
                  'true' == i.attr('rebus') &&
                    (b.append(
                      t("<img src='" + d + "'  style='position: absolute;top:0px;left:0px' />")
                        .width(p)
                        .height(p)
                    ),
                    b.find('img').hide(),
                    (b.data('Use').img = !0)));
          })(),
          (function () {
            let e = null,
              l = i.Cells;
            if (
              (d.y + 1 <= i.Height &&
                !l[d.x][d.y + 1] &&
                o < 2 &&
                ((e = t(a(0, p + 1, u, T, S - p)).appendTo(r)),
                b.css({ borderBottom: '0px' }),
                e.css({ height: '1px', borderTop: 'solid 1px ' + E })),
              d.x + 1 <= i.Width &&
                !l[d.x + 1][d.y] &&
                n < 2 &&
                ((e = t(a(p + 1, 0, i.Settings['grid-background-color'], T - p, S)).appendTo(r)),
                b.css({ borderRight: '0px' }),
                e.css({ width: '1px', borderLeft: 'solid 1px ' + E })),
              0 == i.Settings['thick-border'])
            )
              return !1;
            let c,
              h,
              f,
              g,
              m = p,
              C = p;
            for (c = 0; c < n; c++)
              for (h = 0; h < o; h++) {
                ((f = d.x + c), (g = d.y + h));
                let e = !1,
                  i = !1,
                  n = 3,
                  o = d.x * p - p + c * C,
                  a = d.y * p - p + m * h;
                (l[f][g - 1] ||
                  (t(s(n, C, E, a - n, o, u))
                    .appendTo(r)
                    .css('zIndex', '1'),
                  (e = !0)),
                  l[f][g + 1] ||
                    (t(s(n, C, E, a + m, o, u))
                      .appendTo(r)
                      .css('zIndex', '1'),
                    (i = !0)));
                let b = ((i ? 1 : 0) + (e ? 1 : 0)) * n;
                ((l[f + 1] && l[f + 1][g]) ||
                  t(s(m + b, n, E, a + (e ? -n : 0), o + C, u))
                    .appendTo(r)
                    .css('zIndex', '1'),
                  (l[f - 1] && l[f - 1][g]) ||
                    t(s(m + b, n, E, a + (e ? -n : 0), o - n, u))
                      .appendTo(r)
                      .css('zIndex', '1'));
              }
          })(),
          b.data('isLetter', w),
          w ? b : null
        );
      },
    };
  }
  function n(e, i, n) {
    var o = 0,
      r = 0,
      l = {},
      a = [];
    function s() {
      let i,
        o,
        l = e.AppletSettings.find('clues'),
        a = 0,
        s = {
          SELCOLOR: 'selection-color',
          COMPLETEDCOLOR: 'completed-color',
          CLUECOLOR: 'color',
          URLCOLOR: 'url-color',
          HINTURLTEXT: 'hint-url-text',
          SCROLLCOLOR: 'scroll-color',
          CLUEURLTARGET: 'target-frame',
        };
      for (a in r) ((i = l.attr(a)), null != i && (r[a] = i));
      for (a in ((r['font-family'] = (function (e) {
        let i = e.split(''),
          n = '';
        return (
          t.each(i, function (t, e) {
            e == e.toUpperCase() && 0 != t ? (n += '-' + e) : (n += e);
          }),
          n.toLowerCase()
        );
      })(r['font-family'])),
      s))
        ((o = e.Params[a]), null != o && (r[s[a]] = o));
      t(
        '<style>.ClueCell.Selected{color:' + r['selection-color'] + ' !important;}</style>'
      ).appendTo(n);
    }
    return {
      Words: {},
      WordsWordSearch: {},
      HasKeyWord: !1,
      KeyWordCells: [],
      KeyWordID: {},
      Div: 0,
      Attributes: {
        layout: 'below',
        'font-family': 'sans-serif',
        'font-size': '15',
        width: '100',
        gutter: '5',
        'selection-color': 'red',
        'right-align-numbers': 'true',
        'clue-indent-align': 'true',
        'bold-numbers': 'true',
        'period-with-numbers': 'true',
        'heading-centered': 'false',
        'target-frame': '',
        'hint-url-text': '?',
        'url-color': 'blue',
        'scroll-color': 'gray',
        'completed-color': 'gray',
        color: 'black',
      },
      Start: function (p) {
        ((r = (o = this).Attributes),
          s(),
          e.XMLRect.find('word').each(function (n, r) {
            let l = t(this),
              s = l.attr('x'),
              d = l.attr('y');
            ((o.Words[l.attr('id')] = {
              x: s,
              y: d,
              solution: l.attr('solution'),
              hidden: l.attr('hidden'),
              keyword: l.attr('keyword'),
              cells: l.find('cells'),
              id: l.attr('id'),
              Squares: s ? c({ x: s, y: d }) : [],
              WordSearch: s + '/' + d,
            }),
              e.isWordSearch &&
                (i.Goal++, (o.WordsWordSearch[s + '/' + d] = o.Words[l.attr('id')])),
              'true' == l.attr('keyword') && a.push(o.Words[l.attr('id')]));
          }),
          (function () {
            if (0 == e.AppletSettings.find('clues').length) return !1;
            e.XMLRect.find('clues').each(function (e, i) {
              let n = t(this),
                o = n.find('title');
              ((o = '' != d(o) ? d(o) : o.text()),
                (l[o] = []),
                n.find('clue').each(function (e, i) {
                  let n = t(this),
                    r = {
                      Text: '' != d(n) ? d(n) : n.text(),
                      Word: n.attr('word'),
                      Number: n.attr('number') ? n.attr('number') : '',
                      Format: n.attr('format'),
                      IsLink: n.attr('is-link'),
                      HintUrl: n.attr('hint-url'),
                      Citation: n.attr('citation'),
                    };
                  l[o].push(r);
                }));
            });
          })(),
          (function () {
            if (t.isEmptyObject(l)) return;
            let i = 0,
              a = 0,
              s = r,
              d = s.layout,
              p = parseInt(s['font-size']),
              h = t("<div id='CluesPanel'/>").css({
                fontFamily: s['font-family'],
                fontSize: p,
                border: 0,
                overflow: 'hidden',
                gridArea: 'clues',
              });
            ('below' == d && h.css('padding-top', s.gutter ? s.gutter + 'px' : '2px'),
              (o.Div = h.addClass('Clues').appendTo(n)),
              t.each(l, function (n, r) {
                let l = 'true' == s['heading-centered'] ? 'center' : 'span',
                  p = null,
                  u = 'group-' + a,
                  f = t('<' + l + '/>')
                    .css({
                      height: '' != n ? '10%' : '0px',
                      marginLeft: 'span' == l ? '12px' : '0px',
                      fontSize: '100%',
                    })
                    .addClass('ClueHeading')
                    .attr('id', u)
                    .html(n),
                  g = t('<div/>')
                    .css({
                      'margin-left': '0px',
                      height: '' != n ? '90%' : '100%',
                      'overflow-x': 'hidden',
                      'overflow-y': 'auto',
                    })
                    .addClass('ClueList')
                    .attr({ role: 'listbox', 'aria-labelledby': u })
                    .append(t('<p/>').css({ height: '100px' }));
                (t("<div class='CluesDirec'/>")
                  .css({
                    width: parseInt(s.width) - ('left' == d ? 5 : 0),
                    color: s.color,
                    border: '0px',
                    textAlign: 'left',
                    position: 'relative',
                  })
                  .append(f)
                  .append(g)
                  .appendTo(h),
                  a++,
                  t.each(r, function (n, r) {
                    let l = r.Word ? r.Word : null,
                      a = r.Number,
                      d = o.Words[l],
                      h = t('<p/>').css({
                        position: 'relative',
                        width: '100%',
                        paddingLeft: '1px',
                        paddingBottom: '1px',
                        border: 'solid 1px transparent',
                        wordWrap: 'break-word',
                      });
                    if (
                      (t('<li/>')
                        .attr({ id: 'LI' + l, role: 'option' })
                        .css({
                          'list-style-type': 'none',
                          width: '97%',
                          'margin-top': '3px',
                          'font-weight': 'normal',
                          'text-align': 'left',
                          cursor: 'pointer',
                          position: 'relative',
                        })
                        .data('data', r)
                        .data('index', i)
                        .data('word', l)
                        .data('listDiv', g)
                        .data('wdCoords', d)
                        .data('coordinates', d ? d.x + ',' + d.y : [])
                        .data('Cells', d ? c(d) : [])
                        .append(h)
                        .appendTo(g),
                      i++,
                      null != a && '' != a)
                    ) {
                      let e =
                        parseInt(a) < 10 && 'true' == s['right-align-numbers']
                          ? '&nbsp;' + r.Number + '&nbsp;'
                          : r.Number;
                      ((e += 'true' == s['period-with-numbers'] ? '.&nbsp;' : '&nbsp;'),
                        (p = e),
                        t('<span/>')
                          .css({
                            'font-weight': s['bold-numbers'] ? 'bold' : 'normal',
                            width: '10%',
                          })
                          .html(e)
                          .appendTo(h)
                          .addClass('ClueNumber'));
                    } else
                      null != p &&
                        s['right-align-numbers'] &&
                        t('<span/>')
                          .css({
                            'font-weight': s['bold-numbers'] ? 'bold' : 'normal',
                            width: '10%',
                            visibility: 'hidden',
                          })
                          .html(p)
                          .appendTo(h);
                    (t('<span/>')
                      .css({ fontWeight: 'normal' })
                      .html(r.Text + (null != r.Format ? '&nbsp;(' + r.Format + ')' : ''))
                      .appendTo(h)
                      .addClass('ClueText'),
                      r.HintUrl &&
                        t('<span/>')
                          .css({
                            fontWeight: 'bolder',
                            position: 'absolute',
                            float: 'right',
                            top: '0px',
                            color: s['url-color'] ? s['url-color'] : s.color,
                          })
                          .html('[' + s['hint-url-text'] + ']')
                          .appendTo(h.parent())
                          .addClass('ClueHint')
                          .on('click', function () {
                            e.PuzzleState.ShowProcessedURL(r.HintUrl, s['target-frame'], !1, !1);
                          }));
                  }));
              }));
          })());
      },
      KeyWord: function () {
        if (0 == a.length) return;
        o.HasKeyWord = !0;
        let e = i.Size,
          r = t('<div />')
            .css({
              margin: 'auto',
              flexWrap: 'wrap',
              justifyContent: 'center',
              gridArea: 'keyword',
              display: 'flex',
            })
            .appendTo(n);
        (t.each(a[0].cells, function (n, l) {
          let a = t(this).attr('x'),
            s = t(this).attr('y'),
            d = t('<div/>')
              .css({
                width: e,
                height: e,
                border: 'solid 1px black',
                backgroundColor: 'white',
                cursor: 'pointer',
                margin: 0,
                marginLeft: -1,
              })
              .data('data', l)
              .appendTo(r)
              .on('click', function () {
                i.GridSetCellSelected(a, s);
              });
          (i.DomForSolution.clone().css('font-weight', 'bolder').appendTo(d),
            o.KeyWordCells.push(d),
            (o.KeyWordID[a + '-' + s] = d));
        }),
          r.find('*').css('position', 'relative'));
      },
      SetEventClick: function () {
        n.find('li').on('click', function () {
          let n = t(this);
          ((i.IdWord = n.data('word')),
            e.isWordSearch
              ? (o.ResetLi(), o.SetLiClicked(t(this)))
              : i.ClueAction(n.data('Cells'), n.data('wdCoords')));
        });
      },
      SetReference: function (t) {
        t.find('>p').css({ color: r['selection-color'] });
      },
      SetLiClicked: function (t) {
        let e = r['selection-color'],
          n = t.addClass('Selected').attr('aria-selected', !0),
          o = n.attr('id');
        (i.Input.attr('aria-labelledby', o),
          t.hasClass('ClueCell') ||
            (n.find('>p').css({ border: 'solid 1px ' + e, color: e }),
            n.data('listDiv').attr('aria-activedescendant', o)));
      },
      ResetLi: function () {
        (n
          .find('li')
          .removeClass('Selected')
          .removeAttr('aria-selected')
          .not('.ClueCell')
          .find('>p')
          .css({ border: 'solid 1px transparent', color: r.color }),
          n
            .find('li.IsLink')
            .not('.ClueCell')
            .removeClass('Selected')
            .find('>p')
            .css({ border: '0px', color: r['url-color'] }),
          n
            .find('li.Completed')
            .css({ color: r['completed-color'] })
            .find('>p')
            .css({ color: r['completed-color'] }));
      },
    };
  }
  function o(e, i, n, o) {
    var r = !1,
      a = null,
      s = '%SUBMIT%',
      d = '%MARKED%',
      p = '%PROGRESS%',
      h = '%TIME%',
      u = '%CHARSET%',
      f = '%KEYWORD%',
      g = 0,
      m = 0,
      b = null,
      C = null,
      x = 0,
      w = null,
      v = !1;
    return {
      Words: null,
      LinkFrame: '',
      LinkType: '',
      SubmitURL: '',
      SubmitFrame: '',
      SubmitType: '',
      SaveUrl: '',
      ShowProcessedURL: function (e, i, n, r) {
        let l,
          a,
          c = (function (e, i, n, r) {
            let l = i,
              a = l.indexOf(s);
            if (
              (-1 != a && (l = l.substring(0, a) + e.GetSubmit(r) + l.substring(a + 8)),
              (a = l.indexOf(p)),
              -1 != a && (l = l.substring(0, a) + e.GetProgressString(0, r) + l.substring(a + 10)),
              (a = l.indexOf(d)),
              -1 != a && (l = l.substring(0, a) + e.GetProgressString(2, r) + l.substring(a + 8)),
              (a = l.indexOf(u)),
              -1 != a && (l = l.substring(0, a) + 'UTF8'),
              (a = l.indexOf(h)),
              -1 != a && (l = l.substring(0, a) + e.GetTime() + l.substring(a + 6)),
              (a = l.indexOf(f)),
              -1 != a)
            ) {
              var c = '',
                g = 0;
              (t.each(o.KeyWordCells, function (e, i) {
                (g++, (c += t(this).find('p:eq(0) span:eq(0)').html()));
              }),
                (l = l.substring(0, a) + c + l.substring(a + g)));
            }
            return l;
          })(this, e, 0, r),
          g = c.indexOf('?'),
          m = [];
        (-1 != g ? ((m = c.substring(g + 1).split('&')), (g = c.substring(0, g))) : (g = c),
          i || (i = n ? '_self' : '_blank'),
          'POST' == (r ? 'POST' : 'GET')
            ? ((a = t('<form />').fadeOut().attr({ method: 'POST', target: i, action: g })),
              t.each(m, function (e, i) {
                let n = i.split('=');
                t('<input/>').attr({ name: n[0], value: n[1], hidden: !0 }).appendTo(a);
              }),
              t("<input type='submit' value='post'/>").attr({ hidden: !0 }).appendTo(a),
              a.appendTo('body'),
              (l = t.post(
                g,
                a.serializeArray(),
                function (e, n) {
                  let o = e.substring(4);
                  '_self' == i || 'self' == i
                    ? (window.location = o)
                    : '_blank' == i || 'blank' == i
                      ? window.open(o)
                      : t('#' + i).attr({ src: o });
                },
                'html'
              )),
              l.fail(function () {
                alert(
                  'Error submitting: must have internet connection and be submitting to same website as puzzle page'
                );
              }))
            : '_self' == i || 'self' == i
              ? (window.location = c)
              : '_blank' == i || 'blank' == i
                ? window.open(c)
                : t('#' + i).attr({ src: c }));
      },
      PuzzleCookie: function () {
        let t,
          i,
          n = 0,
          o =
            ((r = e.XmlDoc),
            void 0 !== window.XMLSerializer
              ? new window.XMLSerializer().serializeToString(r)
              : void 0 !== r.xml
                ? r.xml
                : '');
        var r;
        if (0 == o.length) return n;
        for (t = 0, l = o.length; t < l; t++)
          ((i = o.charCodeAt(t)), (n = (n << 5) - n + i), (n |= 0));
        return 'CCPuzApplet_' + n;
      },
      GetCookie: function () {
        if (document.cookie && document.cookie.includes('CCPuzApplet')) {
          const t = this.PuzzleCookie(),
            e = document.cookie.split(';').map((t) => t.trim());
          for (const i of e) {
            const [e, n] = i.split('=').map((t) => t.trim());
            if (e === t)
              try {
                return decodeURIComponent(n);
              } catch (t) {
                return (console.error('Error decoding cookie:', t), null);
              }
          }
        }
        return null;
      },
      SaveCookie: function () {
        !(function (t, e, i) {
          let n = new Date();
          n.setDate(n.getDate() + i);
          let o =
            encodeURIComponent(e) +
            (null == i ? '' : '; expires=' + n.toUTCString()) +
            '; path=' +
            window.location.pathname;
          document.cookie = t + '=' + o;
        })(this.PuzzleCookie(), this.GetProgressString(!1, !0), 30);
      },
      Save: function () {
        this.SaveUrl
          ? this.ShowProcessedURL(this.SaveUrl, this.SubmitFrame, !0, !1)
          : this.SaveCookie();
      },
      Submit: function () {
        (this.SaveCookie(),
          this.HasNoPlaceHolder(this.SubmitURL) && (this.SubmitURL += this.GetSubmit(!1)),
          this.ShowProcessedURL(this.SubmitURL, this.SubmitFrame, !0, 'POST' == this.SubmitType));
      },
      GetSubmit: function (t) {
        return this.GetProgressString(g ? 1 : 0, t);
      },
      GetProgressString: function (t, i) {
        return e.isWordSearch
          ? this.GetWordSearchProgressString(t, i)
          : 0 == t || e.isSudoku
            ? this.GetNonFriendlyProgressString()
            : this.GetFriendlyProgressString(2 == t, i);
      },
      GetNonFriendlyProgressString: function () {
        let t,
          e,
          n = '',
          o = i.Cells;
        for (t = 0; t <= i.Height; t++)
          for (e = 0; e <= i.Width; e++) {
            let i = '',
              r = o[e][t];
            (null != r &&
              '' != r &&
              'letter' == r.data('data').type &&
              ((i = r.data('ObjectLetter').html() ? r.data('ObjectLetter').html() : '-'),
              (i = '*' == r.data('SolveStatus') ? '*' + i : i),
              (i = i.split('').length > 1 ? '|' + i + '|' : i)),
              (n += i));
          }
        return n;
      },
      GetFriendlyProgressString: function (e, n) {
        this.Words = o.Words;
        let r = '',
          l = '',
          a = this,
          s = i.Cells;
        return (
          t.each(o.Words, function (e, i) {
            var o = '1';
            ((r += ' '),
              t.each(i.Squares, function (t, e) {
                let i = e.split('-'),
                  l = s[i[0]][i[1]].data('ObjectLetter').html();
                ((r += '' != l ? a.MayEncode(l, n) : '-'),
                  l != s[i[0]][i[1]].data('data').solution && (o = '0'));
              }),
              t.each(this.cells, function (e, i) {
                let l = c({ x: t(i).attr('x'), y: t(i).attr('y') });
                t.each(l, function (e, i) {
                  let l = i.split('-');
                  t.inArray(l[0] + '-' + l[1], i.Squares) < 0 &&
                    ((Cell = s[l[0]][l[1]].data('ObjectLetter').html()),
                    '' != Cell ? (r += a.MayEncode(Cell, n)) : (r += '-'),
                    Cell != s[l[0]][l[1]].data('data').solution && (o = '0'));
                });
              }),
              (l += o));
          }),
          e ? l + r : r.substring(1)
        );
      },
      GetTime: function () {
        return e.TimerObject.Start;
      },
      HasNoPlaceHolder: function (t) {
        return (
          null == t ||
          (-1 == t.indexOf(s) &&
            -1 == t.indexOf(p) &&
            -1 == t.indexOf(d) &&
            t.indexOf(-1 == h) &&
            -1 == t.indexOf(h))
        );
      },
      SetUrl: function () {
        var t = this,
          i = e.Params,
          n = e.AppletSettings,
          o = n.find('actions'),
          l = o.find('submit'),
          s = o.find('save'),
          d = n.find('completion');
        ((t.SubmitURL = i.SUBMIT || l.attr('target-url') || ''),
          (t.SubmitFrame = i.SUBMITFRAME || l.attr('target-frame') || ''),
          (t.SubmitType = i.SUBMITMETHOD || l.attr('target-type') || ''),
          (t.SaveUrl = i.SAVE || s.attr('target-url') || ''),
          (g = d && 'true' == d.attr('friendly-submit') ? 1 : 0),
          (g = i.hasOwnProperty('FRIENDLYSUBMIT') ? parseInt(i.FRIENDLYSUBMIT) : g),
          d &&
            ((m = d.attr('completion-picture') || 0),
            (b = d.attr('target-url') || ''),
            (C = d.attr('target-frame') || ''),
            (x = d.attr('completion-picture-width') || 0)),
          (m = i.COMPLETIONPICTURE || m),
          (b = i.COMPLETIONPICTUREURL || b),
          (x = i.COMPLETIONPICTUREWIDTH || x),
          (C = i.COMPLETIONPICTUREURLFRAME || C),
          (a = i.FINISHEDURL || (d && d.attr('target-url')) || null),
          (t.LinkFrame = i.FINISHEDURLFRAME || (d && d.attr('target-frame')) || 0),
          (t.LinkType = (d && d.attr('target-type')) || ''),
          (w = (d && d.text()) || ''),
          (r = !(null == d || !d.attr('only-if-correct')) && 'false' != d.attr('only-if-correct')),
          (r = i.COMPLETECORRECT || r));
      },
      GridWord: function (t) {
        var e,
          i,
          n,
          o = t.x.split('-'),
          r = t.y.split('-'),
          l = [],
          a = 1 == o.length ? 'X' : 'Y';
        if ('X' == a)
          for (
            r[0] = parseInt(r[0]),
              r[1] = parseInt(r[1]),
              i = r[0] > r[1] ? r[1] : r[0],
              n = r[0] > r[1] ? r[0] : r[1],
              e = i;
            e <= n;
            e++
          )
            l.push(o[0] + '-' + e);
        if ('Y' == a) {
          ((o[0] = parseInt(o[0])), (o[1] = parseInt(o[1])));
          let t = o[0] > o[1] ? o[1] : o[0];
          for (n = o[0] > o[1] ? o[0] : o[1], e = t; e <= n; e++) l.push(e + '-' + r[0]);
        }
        return l;
      },
      Congratulations: function (t, n) {
        if (v || i._loading) return !1;
        if (r) {
          if (t + n != i.Goal) return !1;
        } else if (i.Goal != i.TotalGoal) return !1;
        ((v = !0),
          '' != e.TimerDiv &&
            (e.TimerDiv.stopTime(), (e.TimerObject.Stop = !0), (e.TimerObject.Stopping = !0)),
          this.PuzzleCompleted());
      },
      PuzzleCompleted: function () {
        m
          ? this.ShowCompletionMessage()
          : null != a
            ? (this.SaveCookie(), this.ShowProcessedURL(a, this.LinkFrame, !0, !1))
            : '' != w && this.ShowCompletionMessage();
      },
      ShowCompletionMessage: function () {
        let o,
          r,
          l,
          a,
          s,
          d = parseInt(e.Attributes.height),
          c = parseInt(e.Attributes.width);
        (m
          ? ((s = t('<img/>')),
            s.load(function () {
              ((o = this.height),
                (r = this.width),
                x && ((o *= x / r), (r = x)),
                (o > d || r > c) && ((l = 0.9 * Math.min(d / o, c / r)), (o *= l), (r *= l)),
                s
                  .css({
                    width: r,
                    height: o,
                    left: 0,
                    right: 0,
                    'margin-left': (c - r) / 2,
                    'margin-top': (d - o) / 2 - 5,
                    cursor: 'pointer',
                  })
                  .appendTo(n));
            }),
            s.attr('src', m).css({ zIndex: '5', position: 'absolute', border: 'solid 5px #c00' }))
          : ((s = t('<div/>')
              .css({
                color: 'darkred',
                'background-color': 'white',
                border: 'solid 5px #c00',
                padding: '5px',
                cursor: 'pointer',
                'text-align': 'center',
                width: 0.8 * c,
                'z-index': 10,
              })
              .addClass('CompleteMsg')),
            (a = t('<span/>')
              .css({ 'font-size': 0.55 * i.Size + 'px', 'font-weight': 'bolder' })
              .html(w)
              .appendTo(s)),
            s.appendTo(n),
            (o = a.height() + 10),
            (r = a.width() + 10),
            s.css({
              width: r,
              height: o,
              position: 'absolute',
              left: 0,
              right: 0,
              'margin-left': (c - r) / 2,
              'margin-top': (d - o) / 3,
            })),
          setTimeout(function () {
            function e() {
              (s.remove(),
                n.off('click', e),
                t(' > *', n).off('click', e),
                b && this.ShowProcessedURL(b, PictureURLFrame, !0, !1));
            }
            (n.on('click', e), t(' > *', n).on('click', e));
          }, 100));
      },
      GetWordSearchProgressString: function (e, i) {
        let n = this,
          r = '',
          l = '';
        return (
          t.each(o.WordsWordSearch, function (t, o) {
            if (null != o.Object && null == o.Reves) {
              ((l += null != o.Real ? '1' : '0'), (r += '+'));
              let a = t.split('/'),
                s = a[0].split('-'),
                d = a[1].split('-');
              (0 != e && (r += n.MayEncode(o.solution, i)),
                (r +=
                  '(' +
                  (parseInt(s[0]) - 1) +
                  ',' +
                  (parseInt(d[0]) - 1) +
                  ',' +
                  (parseInt(s[1]) - 1) +
                  ',' +
                  (parseInt(d[1]) - 1) +
                  ')'));
            }
          }),
          r.length > 0 ? (2 == e ? l + r : r.substring(1)) : ''
        );
      },
      MayEncode: function (t, e) {
        return t;
      },
    };
  }
  function r(i, n) {
    var o = 0,
      r = 0,
      l = 0,
      a = 0,
      s = 0,
      d = 0,
      p = navigator.userAgent,
      f = t('body'),
      g = null,
      m = 0,
      b = 0,
      C = [],
      x = [],
      w = [],
      v = 0,
      y = 0,
      S = 0,
      T = 0,
      E = 3,
      I = 3,
      k = {},
      L = 0,
      O = !1,
      z = 0,
      P = ' ',
      A = !1,
      R = 0,
      M = 0,
      W = 0,
      H = 0,
      D = 0,
      U = 0,
      F = i.Attributes,
      j = null,
      G = 0,
      q = null,
      B = 0,
      _ = {},
      N = [],
      V = 0,
      X = 0,
      $ = 0,
      K = 1,
      Z = 0,
      Y = 0,
      Q = !1,
      J = [],
      tt = 0,
      et = 'Protector',
      it = 'solution',
      nt = p.indexOf('iPhone') >= 0,
      ot = p.indexOf('iPad') >= 0,
      rt = window.visualViewport,
      lt = (navigator.vendor.match(/apple/i) || '').length > 0,
      at = t(
        '<div style="position: fixed;width: 100%;height: 100%;visibility: hidden;"></div>'
      ).appendTo(f),
      st = !1,
      dt = 0,
      ct = 0,
      pt = 0;
    function ht() {
      if (g.is(':visible')) {
        let t = d.Input.offset().top;
        (t > window.innerHeight + window.scrollY || t + b < window.scrollY) && g.hide();
      }
    }
    function ut(t) {
      if (!st && g.is(':visible')) {
        ((st = !0),
          requestAnimationFrame(function () {
            st = !1;
            let t = at.height() - rt.height - rt.offsetTop;
            if (ft()) {
              (g.css({ bottom: t, paddingLeft: 4 + rt.offsetLeft, fontSize: '100%' }),
                g.find('li').css('width', rt.width - 8));
              let e = g.find('li p .ClueText').outerHeight(),
                i = (100 * rt.height) / 5 / e;
              (i < 100 &&
                (g.css('font-size', i + '%'), (e = g.find('li p .ClueText').outerHeight())),
                g.css({ height: e }));
            } else g.hide();
          }));
      }
    }
    function ft() {
      let t = (
        i.Responsive && i.ClueHintPanel.is(':visible') ? i.ClueHintPanel : n
      )[0].getBoundingClientRect();
      return (
        (rt &&
          (rt.width < t.width ||
            rt.height < t.height ||
            t.left + t.width > rt.width ||
            t.top + t.height > rt.height ||
            t.top + t.height / 3 < 0)) ||
        window.innerWidth < t.width ||
        window.innerHeight < t.height
      );
    }
    function gt(t, e) {
      v = { x: t, y: e };
      let i = b / 10;
      (T && T.remove(),
        (T = k.rect(t * b + i, e * b + i, b - 2 * i, b - 2 * i, b / 3)).attr({
          'stroke-width': 2,
          stroke: F['selected-cells-color'],
        }),
        (D = t * b + b / 2),
        (U = e * b + b / 2),
        T.toBack());
    }
    function mt(t) {
      (T.attr({ opacity: 1 }),
        L != t && (0 != L && T.rotate(-L, D, U), T.rotate(t, D, U), (L = t)));
    }
    function bt(e, n) {
      let r = e.toLocaleUpperCase(),
        l = i.isSudoku,
        a = i.isCoded,
        c = S.data('Use'),
        p = c[it];
      if (
        (r.length > 1 && (r = e),
        (r == p || r.toLowerCase() == p || ('i' == e && 'İ' == p) || e.toUpperCase() == p) &&
          (r = p),
        !(F['enforce-alphabet'] || l || a) ||
          !(
            (t.inArray(r, i.Alphabet) < 0 && '' != r) ||
            (l &&
              '' != r &&
              F['validate-sudoku'] &&
              !(function (t) {
                if (d.Pencil) return !0;
                function e(e) {
                  return e.data('ObjectLetter').html() == t && '*' != e.data('SolveStatus');
                }
                let i,
                  n,
                  o = d.Cells,
                  r = parseInt(S.data('data').x),
                  l = parseInt(S.data('data').y),
                  a = r,
                  s = l;
                for (i = 1; i <= d.Width; i++) if (i != l && e(o[r][i])) return !1;
                for (i = 1; i <= d.Height; i++) if (i != r && e(o[i][l])) return !1;
                for (
                  r = r <= E ? 1 : r - (r % E == 0 ? E : r % E) + 1,
                    l = l <= I ? 1 : l - (l % I == 0 ? I : l % I) + 1,
                    i = r;
                  i < r + E;
                  i++
                )
                  for (n = l; n < l + I; n++) if (i != a && n != s && e(o[i][n])) return !1;
                return !0;
              })(r)) ||
            (a &&
              !d.Pencil &&
              !(function (e, i) {
                var n = t.inArray(e, d.LetterUsed);
                if (n >= 0 && '' != e) {
                  if ('' != S.data('ObjectLetter').html() && !d.Background && !Q && !d.Solution) {
                    if (
                      (S.css('background-color', F['selected-cells-color']),
                      0 != F['type-skip-existing'])
                    ) {
                      let t = Y++;
                      for (Y > Z && (Y = 0); '' != N[Y].data('ObjectLetter').html() && t != Y; )
                        ++Y > Z && (Y = 0);
                    } else Y < Z && Y++;
                    S = N[Y];
                  }
                  return !1;
                }
                var o = S.data('ObjectLetter').html();
                (o &&
                  ((d.LetterUsed[t.inArray(o, d.LetterUsed)] = ''),
                  (_[o] = void 0),
                  (d.LetterUsed = t.grep(d.LetterUsed, function (t) {
                    return '' != t;
                  }))),
                  d.LetterUsed.push(e),
                  (_[e] = i),
                  d.RepaintAlphabet());
                return !0;
              })(r, S))
          ))
      ) {
        if (!c.hint || O) {
          S.data(et) && S.data(et).fadeTo('fast', 0);
          let e,
            i,
            n = S.data('ObjectLetter'),
            o = n.html(),
            l = r,
            c = d.FontColor,
            h = d.FontWeight,
            u = d.FontStyle;
          if (
            (d.Pencil
              ? ((u = 'italic'), (h = ''), (c = F['pencil-color']))
              : M || r == p || (c = F['wrong-letter-color'] || c),
            (i = { color: c, 'font-style': u, 'font-weight': h }),
            Q && (r = A ? r : o + r),
            '' == o && '' != r ? d.TotalGoal++ : '' != o && '' == r && d.TotalGoal--,
            S.data('Correct', !1),
            r == p ? o != p && (R++, S.data('Correct', !0)) : o == p && R--,
            Q && (r = A ? r : l),
            (e = d.Pencil && !M ? '*' : !M),
            (r = Q && !A ? n.html() + r : r),
            n.css(i),
            d.DrawSizedLetter(n, r),
            S.data('SolveStatus', e),
            a &&
              t.each(d.CodedLetter[p], function (t, n) {
                var o = n.data('ObjectLetter');
                (o.css(i),
                  n.data('SolveStatus', e),
                  O && (n.data('Use').hint = !0),
                  d.DrawSizedLetter(o, r));
              }),
            (function (e) {
              let i = S.data('data'),
                n = s.KeyWordID[i.x + '-' + i.y];
              n && d.DrawSizedLetter(t(n).find('p span'), e, 1, parseInt(0.75 * b));
            })(r),
            Et(S.data('WordId')),
            O)
          )
            return;
        }
        if (!(d.Background || Q || d.Solution || n)) {
          if (
            (S.css('background-color', F['selected-cells-color']), 0 != F['type-skip-existing'])
          ) {
            let t = Y++;
            for (Y > Z && (Y = 0); '' != N[Y].data('ObjectLetter').html() && t != Y; )
              ++Y > Z && (Y = 0);
          } else Y < Z && Y++;
          S = N[Y];
        }
        (A &&
          !Q &&
          (S.css('background-color', F['selected-cells-color']),
          (S = N[(Y = Y - 1 < 0 ? 0 : Y - 1)])),
          o.Congratulations(R, W));
      }
    }
    function Ct(t) {
      t.x < 0 ||
        t.y < 0 ||
        t.x >= d.Width ||
        t.y >= d.Height ||
        (y && t.x == y.x && t.y == y.y) ||
        ((y = t), zt(t) && T.attr({ opacity: 0 }));
    }
    function xt() {
      if (((L = 0), 0 == T.attr('opacity') || !y || (v.x == y.x && v.y == y.y)))
        return (T.remove(), void (y = 0));
      var t = null,
        e = v.x + 1 + '-' + (y.x + 1) + '/' + (v.y + 1) + '-' + (y.y + 1),
        i = y.x + 1 + '-' + (v.x + 1) + '/' + (y.y + 1) + '-' + (v.y + 1);
      (V.hasOwnProperty(e) ? (t = V[e]) : V.hasOwnProperty(i) && (t = V[i]),
        null != t && null != t.id
          ? (null == t.Object
              ? ((t.Object = T),
                0 == t.Input && W--,
                R++,
                d.TotalGoal++,
                (t.Input = !0),
                n.find('li#LI' + t.id).addClass('Completed'))
              : (t.Object.remove(),
                0 == t.Input ? W-- : R--,
                d.TotalGoal--,
                (t.Input = null),
                n.find('li#LI' + t.id).removeClass('Completed'),
                T.remove(),
                (t.Object = null)),
            o.Congratulations(R, W),
            s.ResetLi())
          : V.hasOwnProperty(e)
            ? (V[e].Object.remove(), T.remove(), delete V[e], delete V[i])
            : V.hasOwnProperty(i)
              ? (V[i].Object.remove(), T.remove(), delete V[e], delete V[i])
              : ('' != F['wrong-letter-color'] && T.attr({ stroke: F['wrong-letter-color'] }),
                (V[e] = { Object: T, Real: !1 }),
                (V[i] = { Object: T, Real: !1, Reves: !0 })),
        (y = 0),
        (T = null));
    }
    function wt(e, i) {
      let n = k.canvas.createSVGPoint();
      return (
        (n.x = e),
        (n.y = i),
        (n.x -= t(window).scrollLeft()),
        (n.y -= t(window).scrollTop()),
        (n = n.matrixTransform(k.canvas.getScreenCTM().inverse())),
        { x: parseInt(n.x / b), y: parseInt(n.y / b) }
      );
    }
    function vt() {
      ((pt = t('<div role="grid"/>').css({ gridArea: 'grid', position: 'relative' }).appendTo(n)),
        (dt || ct) &&
          ((d.Scroll = !0),
          pt.css({
            overflow: 'auto',
            backgroundColor: 'gray',
            borderLeft: 'solid 1px transparent',
            borderTop: 'solid 1px transparent',
            position: 'relative',
          }),
          dt && pt.css({ width: dt - 1 + 'px' }),
          ct && pt.css({ height: ct - 1 + 'px' })));
      let o = e(i, d);
      !(function () {
        let t = i.Params.GRIDBACKCOLOR || u,
          e = pt.fillRect(0, 0, d.Width * b + 1, d.Height * b + 1, { color: t });
        Raphael(e.get(0), d.Width * b, d.Height * b);
      })();
      let r,
        l,
        a,
        s = z.find('cell'),
        c = {},
        p = d.Cells;
      for (
        t.each(s, function (e, i) {
          let n = t(this).attr('x').split('-'),
            o = t(this).attr('y').split('-'),
            a = n.length > 1 ? n[1] - n[0] + 1 : 1,
            s = o.length > 1 ? o[1] - o[0] + 1 : 1,
            d = parseInt(n[0]),
            h = parseInt(o[0]);
          for (r = 0; r < a; r++) for (l = 0; l < s; l++) (r || l) && (p[d + r][h + l] = '?');
          ((p[d][h] = '?'), (c[d + '-' + h] = t(i)));
        }),
          l = 1;
        l <= d.Height;
        l++
      ) {
        let e = t('<div role="row"/>').appendTo(pt);
        for (r = 1; r <= d.Width; r++)
          null != c[r + '-' + l] &&
            ((a = o.make(c[r + '-' + l], m, d.ArrowSettings, e)),
            a &&
              (a.attr('id', 'puz-cell-' + ((l - 1) * d.Height + r - 1)),
              (p[o.x][o.y] = a),
              J.push(a),
              St(a)));
      }
      for (r = 1; r <= d.Width; r++)
        for (l = 1; l <= d.Height; l++) '?' == p[r][l] && (p[r][l] = null);
    }
    function yt() {
      let t = i.Params;
      function e(e, i) {
        t.hasOwnProperty(e) && (m[i] = t[e]);
      }
      (e('GRIDBACKCOLOR', 'grid-background-color'),
        e('GRIDCOLOR', 'grid-line-color'),
        e('BLOCKCOLOR', 'block-color'),
        e('FONTCOLOR', 'font-color'),
        e('NUMCOLOR', 'number-color'),
        e('REVEALEDCOLOR', 'revealed-color'),
        t.hasOwnProperty('NOPOPUPKEYBOARD') && (d.NoFocus = 'false' != t.NOPOPUPKEYBOARD),
        (function (t) {
          if (!t) return;
          let e,
            i = !1,
            n = '';
          if (r)
            for (d.Progress = t.split(/\).?\(/g), e = 0; e < d.Progress.length; ++e)
              d.Progress[e] = d.Progress[e].replace(/[\(\)]/g, '');
          else
            for (t = t.split(''), e = 0; e < t.length; e++)
              ('|' == t[e] || i ? (i = !0) : d.Progress.push({ solution: t[e], Pencil: !1 }),
                i && '|' != t[e] && '*' != t[e] && (n += t[e]),
                '|' == t[e] &&
                  '' != n &&
                  (d.Progress.push({ solution: n, Pencil: !0 }), (n = ''), (i = !1)));
        })(t.PROGRESS || o.GetCookie()));
    }
    function St(e) {
      if (
        (t(e).on('click', function (e) {
          let n = t(this);
          i.RunTimer();
          try {
            (1 == Q && S.get(0) == this && B) || (Q = !1);
          } catch (e) {
            Q = !1;
          }
          return (
            '' != S &&
              1 != Q &&
              S.data('data').x == n.data('data').x &&
              S.data('data').y == n.data('data').y &&
              (K = !K),
            (S = n),
            l ? (Lt(), (N = new Array(S))) : Tt(),
            Ot(),
            kt(),
            !1
          );
        }),
        B)
      ) {
        t(e)
          .on('touchstart', function (t) {
            1 == t.originalEvent.touches.length &&
              S.get(0) == this &&
              (q = window.setTimeout(function () {
                (alert('Multiletter On'), (Q = !0));
              }, 1e3));
          })
          .on('touchend touchmove', function () {
            (clearTimeout(q), (q = null));
          });
      }
    }
    function Tt() {
      if (
        (Lt(),
        (C = []),
        (x = []),
        (w = []),
        1 == (N = K ? t.merge(Mt(-1, 0), Mt(1, 0)) : t.merge(Mt(0, -1), Mt(0, 1))).length &&
          (null == S.data('Unique') || '' == S.data('Unique')))
      ) {
        let e = 0;
        ((WordId = S.data('WordId')),
          WordId &&
            t.each(WordId, function (t, i) {
              1 == s.Words[i].Squares.length && ((X = i), (e = 1));
            }),
          e || (S.data('Unique', 'Y'), (K = !K), Tt()));
      }
      ((C =
        (x.length > 1 && x[0] == x[1]) || (1 == x.length && 1 == w.length && !K)
          ? x[0] + ',' + w[0] + '-' + w[w.length - 1]
          : x[0] + '-' + x[x.length - 1] + ',' + w[0]),
        S.data('Unique', ''),
        (function () {
          if (null != S.data('WordItem') && null == S.data('ImLink')) {
            let e = C.split(','),
              i = c({ x: e[0], y: e[1] });
            t.each(s.Words[X].cells, function (e, n) {
              let o = c({ x: t(n).attr('x'), y: t(n).attr('y') });
              t.each(o, function (e, n) {
                let o = n.split('-');
                t.inArray(o[0] + '-' + o[1], i) < 0 &&
                  (i.push(o[0] + '-' + o[1]), N.push(d.Cells[o[0]][o[1]]));
              });
            });
          }
        })(),
        (function () {
          let e = !1;
          if (
            (S.data('ImLink') &&
              t.each(S.data('WordId'), function (i, n) {
                let o = s.Words[n],
                  r = o.cells;
                t.each(r, function (i, n) {
                  let l = t(this).attr('x') + ',' + t(this).attr('y');
                  if (C == l) {
                    X = o.id;
                    let i = c({ x: r.attr('x'), y: r.attr('y') }),
                      n = [],
                      l = [],
                      a = !1;
                    (t.each(o.Squares, function (e, o) {
                      let r = o.split('-');
                      t.inArray(o, i) < 0 && (n.push(d.Cells[r[0]][r[1]]), Y++);
                    }),
                      t.each(o.cells, function (e, i) {
                        let o,
                          r = t(this),
                          s = r.attr('x') + ',' + r.attr('y');
                        C == s
                          ? (a = !0)
                          : ((o = c({ x: r.attr('x'), y: r.attr('y') })),
                            t.each(o, function (t, e) {
                              var i = e.split('-');
                              ((a ? l : n).push(d.Cells[i[0]][i[1]]), a || Y++);
                            }));
                      }),
                      (N = t.merge(n, N)),
                      (N = l.length > 0 ? t.merge(N, l) : N),
                      (e = !0));
                  }
                });
              }),
            !l && null != N[1])
          ) {
            let i = N[0].data('WordId'),
              n = N[1].data('WordId');
            if (
              (t.each(i, function (e, i) {
                t.inArray(i, n) > -1 && (X = i);
              }),
              !e && (N[1].data('ImLink') || N[0].data('ImLink')))
            ) {
              let e = s.Words[X].cells.eq(0);
              t.each(e, function (i, n) {
                let o = c({ x: e.attr('x'), y: e.attr('y') }),
                  r = [];
                (t.each(s.Words[X].Squares, function (e, i) {
                  var n = i.split('-');
                  t.inArray(i, o) < 0 &&
                    (d.Cells[n[0]][n[1]].css({ backgroundColor: F['selected-cells-color'] }),
                    r.push(d.Cells[n[0]][n[1]]),
                    Y++);
                }),
                  S.css({ backgroundColor: F['cursor-color'] }),
                  (N = t.merge(r, N)));
              });
            }
          }
        })(),
        (Z = N.length - 1),
        t.each(N, function (t, e) {
          e.css('background-color', F['selected-cells-color']);
        }));
    }
    function Et(e) {
      null != e &&
        t.each(e, function (e, i) {
          var n = s.Words[i].Squares;
          t.each(s.Words[i].cells, function (e, i) {
            n = t.merge(c({ x: t(this).attr('x'), y: t(this).attr('y') }), n);
          });
          var o = !0;
          (t.each(n, function (t, e) {
            var i = e.split('-');
            '' == d.Cells[i[0]][i[1]].data('ObjectLetter').html() && (o = !1);
          }),
            o ? t('li#LI' + i).addClass('Completed') : t('li#LI' + i).removeClass('Completed'));
        });
    }
    function It(t) {
      if (!isNaN(i.MaxCheat) && -1 != i.MaxCheat && H < i.MaxCheat) H++;
      else if (-1 != i.MaxCheat)
        return (
          t.fadeTo('fast', 0.5),
          Action.hasOwnProperty('reveal-word') && Action['reveal-word'].fadeTo('fast', 0.5),
          !1
        );
      return !0;
    }
    function kt() {
      let e = d.Input,
        i = t(window);
      if (
        ((d.NoFocus && B) ||
          (e.trigger('focus'),
          e.is(':focus') || (e.css({ width: '1px', height: '1px' }), e.trigger('focus'))),
        g)
      ) {
        let t = e.offset().top,
          n = g.offset().top;
        g.is(':visible') && t > n && i.scrollTop(i.scrollTop() + t - n + b);
      }
    }
    function Lt() {
      t.each(N, function (t, e) {
        ((1 != e.data('Correct') && e.data('Use').img) || e.find('img').show(),
          e.css('background-color', e.data('background-color')));
      });
    }
    function Ot() {
      S ||
        (function (t) {
          throw (console && console.error && console.error(t), t);
        })(new Error('CellSelected is Undefined'));
      let e,
        o = 0;
      if (
        (S.css('background-color', F['cursor-color']).find('img').hide(),
        l && (Lt(), (N = [S.css('background-color', F['cursor-color'])])),
        s.ResetLi(),
        (e = S.offset()),
        h && (o = (b / 2) * 0.8),
        d.Input.offset({ top: e.top + o, left: e.left }).attr('value', S.find('p span').text()),
        !l &&
          null != S.data('LIS') &&
          (t.each(S.data('LIS'), function (e, o) {
            t.each(o, function () {
              let e = t(this);
              if (!e.data('coordinates')) return !1;
              (e.hasClass('ClueCell') || s.SetReference(e),
                e.data('data').IsLink ||
                  e.data('coordinates') != C ||
                  (e.hasClass('ClueCell') && (s.ResetLi(), s.SetReference(e)),
                  (function (e) {
                    let n = !e.hasClass('ClueCell'),
                      o = n && ft();
                    if (n && i.Responsive) {
                      let n = e
                        .find('p:first')
                        .clone()
                        .css({ width: '100%', marginTop: '', height: 'auto' });
                      (n
                        .find('*')
                        .addBack()
                        .each(function () {
                          t(this).css({ height: '', position: '' });
                        }),
                        i.ClueHintPanel.empty().append(n));
                    }
                    if (!g) {
                      if (!o || (lt && !rt)) return void s.SetLiClicked(e);
                      (t(
                        '<style>#CurrentClueHint *{margin:0;padding:0;line-height: 1.1} #CurrentClueHint{border-top:solid 1px gray;;padding:4px;padding-right:16px;position:fixed;bottom:0;left:0;width:100%;box-sizing:content-box}</style>'
                      ).appendTo(f),
                        (g = t(
                          "<div id='CurrentClueHint' class='Clues ClueHint' aria-hidden='true'></div>"
                        ).appendTo(f)),
                        p.indexOf('iPhone OS 15_0') >= 0
                          ? g.css({ 'padding-bottom': '17px' })
                          : p.indexOf('iPhone OS 15_1') >= 0 &&
                            g.css({ 'padding-bottom': '24px', 'margin-bottom': '-24px' }),
                        rt &&
                          (at.appendTo(f),
                          rt.addEventListener('scroll', ut),
                          rt.addEventListener('resize', ut)));
                    }
                    if (o) {
                      let i = e.clone().css({ width: 'auto', marginTop: '', height: 'auto' });
                      (g.empty().append(i).show(), rt ? ut() : t(document).on('scroll', ht));
                    } else (g.hide(), rt || t(document).off('scroll', ht));
                    s.SetLiClicked(e);
                  })(e)));
              let o = e.parent(),
                r = e[0].getBoundingClientRect(),
                l = o[0].getBoundingClientRect(),
                a = window
                  .getComputedStyle(n[0])
                  .getPropertyValue('transform')
                  .match(/matrix\(([^)]+)\)/),
                d = 1;
              (a && (d = parseFloat(a[1].split(',')[3])),
                r.top < l.top
                  ? o.scrollTop((e.offset().top - o.offset().top) / d + o.scrollTop() - 5)
                  : r.top + r.height > l.top + l.height &&
                    o.scrollTop(
                      (e.offset().top - o.offset().top) / d +
                        o.scrollTop() -
                        o.height() +
                        e.height() +
                        5
                    ));
            });
          }),
          dt || ct))
      ) {
        let t = N[Z].data('data'),
          e = S.data('data'),
          i = d.Size;
        ((t.x * i > pt.width() - 25 || (e.x - 1) * i < pt.scrollLeft()) &&
          pt.scrollLeft((e.x - 1) * i),
          (t.y * i > pt.height() - 25 || (e.y - 1) * i < pt.scrollTop()) &&
            pt.scrollTop((e.y - 1) * i));
      }
    }
    function zt(t) {
      let e = 0.85;
      if (v.x == t.x)
        return (
          T.attr({ height: Math.abs(t.y - v.y) * b + b * e }),
          v.y > t.y ? mt(180) : mt(0),
          !1
        );
      if (v.y == t.y)
        return (
          T.attr({ height: Math.abs(t.x - v.x) * b + b * e }),
          v.x > t.x ? mt(90) : mt(270),
          !1
        );
      if (
        (T.attr({
          height: parseInt(Math.sqrt(b * b * 2)) * (Math.abs(t.x - v.x) + 1) - 2 * b * (1 - e),
        }),
        t.x > v.x)
      ) {
        if (v.y == t.y + (t.x - v.x)) return (mt(225), !1);
        if (v.y == t.y - (t.x - v.x)) return (mt(315), !1);
      } else {
        if (v.y == t.y + (t.x - v.x)) return (mt(45), !1);
        if (v.y == t.y - (t.x - v.x)) return (mt(135), !1);
      }
      return !0;
    }
    function Pt() {
      let e = navigator.userAgent,
        o = !0;
      if (r) return !1;
      function l(t) {
        if (0 == t.which || 8 == t.which) return !0;
        (i.RunTimer(),
          d.DrawLetter(String.fromCharCode(t.which), t.which, t),
          o && t.preventDefault());
      }
      function a(e) {
        (t.inArray(e.which, [37, 38, 39, 40, 46, 45, 8]) > -1 || (73 == e.which && e.ctrlKey)) &&
          (d.DrawLetter(String.fromCharCode(e.which), e.which, e), o && e.preventDefault());
      }
      let s = e.indexOf('Android') >= 0,
        c = e.indexOf('OS 3_2 like Mac') >= 0 || (s && e.indexOf('Chrome') >= 0),
        p = d.Input.css({
          position: 'absolute',
          'z-index': '-10000',
          overflow: 'hidden',
          background: 'transparent',
          display: 'block',
          'font-size': '1px',
          border: 'none',
          'box-shadow': 'none',
          '-moz-box-shadow': 'none',
          '-webkit-box-shadow': 'none',
          color: 'transparent',
          opacity: '0',
          width: '1px',
          height: '1px',
        })
          .appendTo(n)
          .attr({ autocorrect: 'off', spellcheck: 'false', autocomplete: 'off' });
      (e.indexOf('Fennec') >= 0 || (s && e.indexOf('Firefox') >= 0) || c
        ? ((o = !1),
          (function (t, e, i) {
            let n;
            function o() {
              let e,
                n,
                o,
                r = t.val() || '',
                l = P;
              if (r.length > l.length)
                for (n = r.substring(l.length), e = 0; e < n.length; ++e)
                  i.call(t.get(0), { which: n.charCodeAt(e) });
              else if (r.length < l.length)
                for (o = l.length - r.length, e = 0; e < o; ++e) i.call(t.get(0), { which: 8 });
              (r.length <= 0 && ((r = ' '), t.val(r)), (P = r));
            }
            t.on('focus', function () {
              void 0 === n && ((P = t.val() || ''), (n = setInterval(o, e)));
            }).on('blur', function () {
              void 0 !== n && (clearInterval(n), (n = void 0), t.val(' '), (P = ' '));
            });
          })(p, 40, function (t) {
            8 == t.which ? a.apply(d, arguments) : l.apply(d, arguments);
          }))
        : p
            .on('keypress', l)
            .on('keydown', a)
            .on('compositionend', function (t) {
              (i.RunTimer(), d.DrawLetter(t.originalEvent.data, 0, null));
            }),
        p
          .on('focus', function () {
            S.css('background-color', F['cursor-color']);
          })
          .on('blur', function () {
            S.css('background-color', F['selected-cells-color']);
          }),
        (s || nt || ot) &&
          (c || p.css({ width: '0px', height: '0px' }),
          (nt || ot || s) && p.css('font-size', '16px')),
        h && p.css('font-size', '0px'),
        B && p.css({ top: n.offset().top + 'px', left: F.width / 2 + 'px' }));
    }
    function At(t) {
      (l ? (Lt(), (N = new Array(S))) : Tt(), bt(t, !0));
    }
    function Rt(e) {
      ((d.FontColor = 0 != m['revealed-color'] ? m['revealed-color'] : m['font-color']),
        (d.FontStyle = ''),
        (d.FontWeight = 'bolder'));
      let i = d.Pencil;
      if (((d.Pencil = !1), (M = !0), r && 0 != d.IdWord)) d.RevealWordSearch();
      else {
        {
          let i,
            o = null,
            r = [],
            l = S;
          for (i = 0; i < e.length; i++) {
            o = e[i].data('Use');
            var n = o[it];
            (e[i].data('ObjectLetter'),
              e[i].data('Correct', !0),
              e[i].data(et) && e[i].data(et).css({ opacity: 0 }),
              o.img && e[i].find('img').show(),
              a
                ? (_[n] && ((S = _[n]), At('')),
                  (S = e[i]),
                  At(n),
                  (r = t.merge(r, N[i].data('WordId'))))
                : ((S = e[i]), bt(n, !0), (r = t.merge(r, S.data('WordId')))));
          }
          (l && ((S = ''), l.trigger('click')), (r = t.uniqueSort(r)), Et(r), B || kt());
        }
        ((M = !1), i && (d.Pencil = !0));
      }
    }
    function Mt(e, i) {
      let n,
        o = S,
        r = o.data('data'),
        l = r.x,
        a = r.y,
        s = [],
        c = o.data('WordId') ? o.data('WordId') : [],
        p = 1,
        h = '';
      for (
        ;
        ((e > 0 && ++l <= d.Width) ||
          (e < 0 && l-- > 0) ||
          (i > 0 && a++ < d.Height) ||
          (i < 0 && a-- > 0)) &&
        p;

      )
        ((h = d.Cells[l][a]),
          (p = 0),
          null != h &&
            '' != h &&
            ((n = h.data('WordId')),
            null != n &&
              t.each(c, function (e, i) {
                p || (t.inArray(i, n) >= 0 && ((p = 1), s.push(h), (X = i), x.push(l), w.push(a)));
              })));
      return (
        (i < 0 || e < 0) &&
          ((Y = s.length),
          (s = s.reverse()),
          s.push(S),
          x.reverse(),
          x.push(r.x),
          w.reverse(),
          w.push(r.y)),
        s
      );
    }
    return {
      CodedHint: [],
      FontSize: 0,
      NumberSize: 0,
      IdWord: 0,
      CodedLetter: {},
      Progress: [],
      Scroll: !1,
      Solution: !1,
      TotalGoal: 0,
      Goal: 0,
      Shift: !1,
      NoFocus: !1,
      LetterUsed: [],
      Pencil: !1,
      Input: t('<input autocomplete="off" aria-autocomplete="none"/>'),
      XML: {},
      Cells: [],
      Cell: {},
      CellSelected: function () {
        return S;
      },
      Size: 0,
      FontColor: 'black',
      FontStyle: '',
      FontWeight: 'bolder',
      DomForSolution: t('<p/>')
        .css({
          width: '100%',
          textAlign: 'center',
          fontFamily: 'sans-serif',
          fontWeight: 'normal',
          position: 'absolute',
        })
        .append(t('<span/>')),
      Settings: {
        'numbered-sides': { top: 0, left: 0 },
        'italian-style': !1,
        'bars-in-collocations': '?',
        'thick-border': !1,
        'numbering-schema': 'normal',
        'cell-size-in-pixels': 21,
        'grid-line-color': 'black',
        'grid-background-color': 'white',
        'block-color': 'black',
        'font-color': 'black',
        'number-color': 'black',
        'clue-background-color': 'white',
        'clue-foreground-color': '',
        'clue-square-divider-width': 1,
        'revealed-color': !1,
      },
      ArrowSettings: {
        stem: 0.1,
        'head-width': 0.1,
        'head-length': 0.1,
        'bend-start': 0.2,
        'bend-end': 0.1,
        'bend-side-offset': 0.1,
      },
      Start: function (e) {
        ((d = this),
          (s = i.Clues),
          (V = s.WordsWordSearch),
          (o = i.PuzzleState),
          (r = i.isWordSearch),
          (l = i.isSudoku),
          (a = i.isCoded),
          (z = i.XMLGame.find('grid')),
          (m = d.Settings),
          (d._loading = 0),
          (d.XML = e),
          (function () {
            let e = i.XMLGame,
              o = e.find('grid-look');
            (t.each(m, function (t, e) {
              'numbered-sides' != t && null != o.attr(t) && (m[t] = o.attr(t));
            }),
              l && ((I = parseInt(e.attr('box-height'))), (E = parseInt(e.attr('box-width')))),
              (b = parseInt(m['cell-size-in-pixels'])),
              (d.Size = b),
              (d.FontSize = parseInt(10 * b * (F['hide-numbers'] ? 0.75 : 0.65)) / 10),
              (d.NumberSize = parseInt(0.38 * b * 10) / 10),
              yt(),
              (d.FontColor = m['font-color']),
              (dt = F['scroll-width']),
              (ct = F['scroll-height']),
              n.prepend(
                t(
                  '<style>rect{transform-origin: 0 0};.ClueCell{color:' +
                    (m['clue-foreground-color'] || d.FontColor) +
                    '}</style>'
                )
              ));
          })(),
          (_isTouch =
            'ontouchstart' in window ||
            (window.DocumentTouch && document instanceof DocumentTouch) ||
            window.navigator.maxTouchPoints > 0));
        try {
          (document.createEvent('TouchEvent'), (B = !0));
        } catch (t) {}
        if (
          ((function () {
            let t,
              e,
              o,
              r = 'true' == m['thick-border'],
              l = n.parent().width();
            for (
              d.Width = parseInt(z.attr('width')),
                d.Height = parseInt(z.attr('height')),
                d.ViewHeight = ct || b * d.Height + (r ? 7 : 1),
                d.ViewWidth = dt || b * d.Width + (r ? 7 : 1),
                i.Responsive &&
                  rt &&
                  !dt &&
                  d.ViewWidth * i.MinScale > l &&
                  !i.isWordSearch &&
                  ((dt = 0.98 * l), (d.ViewWidth = dt)),
                o = 0;
              o <= d.Width;
              o++
            ) {
              for (e = [], t = 0; t <= d.Height; t++) e.push('');
              d.Cells.push(e);
            }
          })(),
          (function () {
            let e = i.XMLGame.find('arrows');
            if (0 == e.length) return !1;
            t.each(d.ArrowSettings, function (t, i) {
              e.attr(t) && (d.ArrowSettings[t] = parseFloat(i));
            });
          })(),
          vt(),
          (d.Div = pt),
          (function () {
            let e = i.XMLGame.find('numbered-sides'),
              n = 'true' == m['thick-border'] ? b + 2 : b;
            if (e.length > 0) {
              if (null != e.attr('top')) {
                let i = e.attr('top').split(',');
                ((m['numbered-sides'].top = i),
                  t.each(i, function (e, i) {
                    if (e >= d.Width) return !1;
                    pt.fillRect(e * b, -n, b, b, { color: u }).append(
                      t('<p/>')
                        .css({
                          width: b + 'px',
                          fontFamily: 'sans-serif',
                          marginTop: '9px',
                          'text-align': 'center',
                          fontSize: parseInt(0.5 * b) + 'px',
                        })
                        .html(i)
                    );
                  }));
              }
              if (null != e.attr('left')) {
                let i = e.attr('left').split(',');
                ((m['numbered-sides'].left = i),
                  t.each(i, function (e, i) {
                    if (e >= d.Height) return !1;
                    pt.fillRect(-n, e * b, b, b, { color: u }).append(
                      t('<span/>')
                        .css({
                          float: 'right',
                          marginTop: parseInt(0.25 * b) + 'px',
                          marginRight: '4px',
                          fontFamily: 'sans-serif',
                          fontSize: parseInt(0.5 * b) + 'px',
                        })
                        .html(i)
                    );
                  }));
              }
            }
          })(),
          s.Div && i.RespaceClues(),
          !r)
        )
          return (Pt(), !1);
        !(function () {
          let t,
            e = b * d.Width,
            n = b * d.Height;
          ((tt = pt.fillRect(0, 0, e, n, { color: u })),
            (k = Raphael(tt.get(0), e, n))
              .rect(0, 0, e, n)
              .attr({ opacity: 0, fill: 'red' })
              .drag(
                function (t, e, i, n) {
                  Ct(wt(i, n));
                },
                function (t, e) {
                  let n = wt(t, e);
                  (i.RunTimer(), gt(n.x, n.y));
                },
                function (t, e) {
                  xt();
                }
              ),
            !B ||
              (r && p.indexOf('Firefox') >= 0) ||
              ((t = pt.fillRect(0, 0, e, n, { alpha: 0, color: u })),
              p.indexOf('Chrome') >= 0 &&
                t.on('mousemove', function (e) {
                  (t.remove(), (B = 0));
                }),
              t
                .on('click', function (t) {
                  t.preventDefault();
                })
                .on('touchstart', function (t) {
                  var e = t;
                  1 == e.originalEvent.touches.length &&
                    (j = window.setTimeout(function (t) {
                      (i.RunTimer(), (G = 1));
                      var n = e.originalEvent.touches[0],
                        o = wt(n.pageX, n.pageY);
                      (($ = k.circle((o.x + 0.5) * b, (o.y + 0.5) * b, 0.8 * b)).attr({
                        fill: 'red',
                        opacity: 0.5,
                      }),
                        gt(o.x, o.y));
                    }, 300));
                })
                .on('touchmove', function (t) {
                  (clearTimeout(j),
                    G &&
                      ($.attr({ opacity: 0 }),
                      t.preventDefault(),
                      Ct(wt(t.originalEvent.touches[0].pageX, t.originalEvent.touches[0].pageY))));
                })
                .on('touchend', function () {
                  (clearTimeout(j), G && ($.remove(), (G = 0), xt()));
                })
                .on('touchcancel', function () {
                  (clearTimeout(j), G && ($.remove(), T.remove(), (y = 0), (G = 0)));
                })));
        })();
      },
      FirstTime: function () {
        t(window).scrollTop() + t(window).height() >= J[0].offset().top &&
          ((K = J[0] != S), J[0].trigger('click'));
      },
      ClueAction: function (t, e) {
        if (t && t.length > 0) {
          let i = t[0].split('-'),
            n = K;
          ((K = e.x.split('-').length > 1),
            S && S.data('data').x == i[0] && S.data('data').y == i[1] && (K = n != K ? n : K),
            d.Cells[parseInt(i[0])][parseInt(i[1])].trigger('click'));
        }
      },
      GridSetCellSelected: function (t, e) {
        ((S = d.Cells[t][e]), Tt(), Ot(), kt(), d.Input.get(0).scrollIntoView());
      },
      DrawLetter: function (e, o, r) {
        if (t.inArray(o, [37, 38, 39, 40]) > -1)
          return (
            (function (t, e) {
              let o = S.data('data'),
                r = parseInt(o.y),
                l = parseInt(o.x),
                a = l,
                s = r,
                c = !0,
                p = !0,
                h = 1 == K;
              for (
                i.isCoded && (e = !1),
                  e
                    ? ((40 == t && K) ||
                        ((37 == t || 39 == t) && !K) ||
                        (K && 38 == t && 0 != Y)) &&
                      (c = !1)
                    : (K = 40 != t && 38 != t);
                c;

              )
                (((40 == t && ++r > d.Height) ||
                  (38 == t && 0 == --r) ||
                  (39 == t && ++l > d.Width) ||
                  (37 == t && 0 == --l)) &&
                  ((c = !1), (p = !0)),
                  c &&
                    null != d.Cells[l][r] &&
                    '' != d.Cells[l][r] &&
                    ('' != S.data('ObjectLetter').html()
                      ? d.Cells[l][r].trigger('click')
                      : h != K
                        ? ((K = !K), d.Cells[a][s].trigger('click'))
                        : d.Cells[l][r].trigger('click'),
                    (c = p = !1)));
              if (e && p) {
                let e,
                  i = n.find('li.Selected');
                if (1 == i.length) {
                  if (40 == t || 39 == t)
                    return (
                      (e = n.find('li').eq(i.data('index') + 1)),
                      0 == e.length && (e = n.find('li:first')),
                      void e.trigger('click')
                    );
                  (38 != t && 37 != t) ||
                    ((e = n.find('li').eq(i.data('index') - 1)),
                    0 == e.length && (e = n.find('li:last')),
                    e.trigger('click'));
                }
              }
            })(o, r.shiftKey),
            !1
          );
        switch (o) {
          case 13:
            Q = !1;
            var s = n.find('li').index(n.find('li.Selected').eq(0));
            ((s = r.shiftKey
              ? 0 == s
                ? n.find('li').length - 1
                : s - 1
              : s + 1 < n.find('li').length
                ? s + 1
                : 0),
              n.find('li').eq(s).trigger('click'));
            break;
          case 46:
            bt('', !0);
            break;
          case 32:
          case 27:
            bt('', !1);
            break;
          case 45:
            if (!l) {
              if (a && !this.Pencil) return !1;
              Q = !Q;
            }
            break;
          case 8:
            let t = S.data('ObjectLetter').html();
            ((t = t.split('')),
              (A = !0),
              (t = (t.length > 1 ? t.slice(0, t.length - 1) : ['']).join('')),
              bt(t, !0),
              (A = !1));
            break;
          default:
            if (r && (r.metaKey || r.ctrlKey) & (73 == r.which) && !l) {
              if (a && !this.Pencil) return !1;
              Q = !Q;
            } else bt(e, !1);
        }
        (Ot(), kt());
      },
      DrawSizedLetter: function (t, e, n, o) {
        ((n = n || l || r || i.Attributes['hide-numbers']), (o = o || d.FontSize));
        let a = t.parent(),
          s = r ? 0 : n ? 2 : d.NumberSize - 1;
        if (
          (t.css({ fontSize: o + 'px', 'line-height': 1, 'white-space': 'nowrap' }).html(e),
          e.length > 1)
        ) {
          let e = t.width();
          e > b - 3 && ((o *= b / e - 0.1), t.css({ fontSize: o + 'px' }));
        }
        (a.css({ 'margin-top': s + 'px', fontSize: '1px' }),
          o < b - s && t.css('line-height', b - s + 'px'));
      },
      RepaintAlphabet: function () {
        t.each(i.LetterAlphabet, function (e, i) {
          t.inArray(t(this).html(), d.LetterUsed) >= 0
            ? t(this).fadeTo('fast', 0.5)
            : t(this).fadeTo('fast', 1);
        });
      },
      LoadProgress: function () {
        let t,
          e,
          i,
          n = d.Progress;
        if (r)
          for (t = 0; t < n.length; t++)
            ((i = n[t].split(',')),
              '' != i[0] &&
                (gt(parseInt(i[0]), parseInt(i[1])),
                Ct({ x: parseInt(i[2]), y: parseInt(i[3]) }),
                xt(),
                i.shift()));
        else {
          for (d._loading = 1, t = 1; t <= d.Height; t++)
            for (e = 1; e <= d.Width; e++)
              null != d.Cells[e][t] &&
                '' != d.Cells[e][t] &&
                (null != n[0] && '-' != n[0].solution
                  ? (n[0].Pencil && (d.Pencil = !0),
                    (S = d.Cells[e][t]),
                    At(n[0].solution),
                    n.shift(),
                    (d.Pencil = !1),
                    (d.FontStyle = ''),
                    (d.FontWeight = 'bolder'),
                    (d.FontColor = m['font-color']))
                  : null != n[0] && '-' == n[0].solution && n.shift());
          d._loading = 0;
        }
      },
      ButtonActions: {
        revert: function () {
          var e;
          (s.Div &&
            s.Div.find('li').removeClass('Completed').find('p').css({ color: s.Attributes.color }),
            r
              ? t.each(V, function (t, e) {
                  (null != e.Object &&
                    (e.Object._raph_removed || (e.Object.remove(), (e.Object._raph_removed = !0)),
                    (e.Object = null),
                    (e.Input = null)),
                    null != e.Real && delete V[t]);
                })
              : ((e = S),
                t.each(J, function (e, i) {
                  let n = t(this);
                  1 != n.data('Use').hint &&
                    (n.find('img').hide(),
                    n.data('ObjectLetter').html() &&
                      ((S = n), At(''), n.data(et) && n.data(et).css({ opacity: 0 })));
                }),
                e && ((S = ''), e.trigger('click')),
                kt()),
            (R = 0),
            (W = 0),
            (d.TotalGoal = 0));
        },
        check: function () {
          if (
            (r &&
              t.each(V, function (t, e) {
                0 == e.Real &&
                  (e.Object._raph_removed || (e.Object.remove(), (e.Object._raph_removed = !0)),
                  delete V[t]);
              }),
            kt(),
            r)
          )
            return !1;
          t.each(J, function (e, i) {
            $this = t(this);
            var n = $this.data('ObjectLetter').html();
            '' != n &&
              $this.data('Use')[it] != n &&
              ($this.data(et) ||
                (function (e) {
                  if (e.data('isLetter')) {
                    var i = e.fillRect(0, 0, b, b, { color: u });
                    (i
                      .css({
                        textAlign: 'center',
                        fontFamily: 'sans-serif',
                        fontSize: 1.1 * b + 'px',
                        color: 'red',
                        fontWeight: 'normal',
                      })
                      .append(t('<div/>').css({ opacity: '0' }).html('X')),
                      e.data(et, i.find('div:eq(0)')));
                  }
                })($this),
              $this.data(et) && $this.data(et).fadeTo('fast', 1));
          });
        },
        save: function () {
          o.Save();
        },
        submit: function () {
          o.Submit();
        },
        'reveal-word': function () {
          return !!It(t(this)) && (Rt(N), !1);
        },
        'reveal-letter': function () {
          return !!It(t(this)) && (Rt(new Array(S)), !1);
        },
        solution: function () {
          if (
            (s.Div &&
              s.Div.find('li')
                .addClass('Completed')
                .find('p')
                .css({ color: s.Attributes['completed-color'] }),
            r)
          )
            return (
              t.each(V, function (t, e) {
                if ((null != e.Object && (e.Object.remove(), (e.Object = null)), null == e.Real)) {
                  var i = t.split('/'),
                    n = i[0].split('-'),
                    o = i[1].split('-');
                  (gt(n[0] - 1, o[0] - 1),
                    (y = { x: n[1] - 1, y: o[1] - 1 }),
                    zt({ x: n[1] - 1, y: o[1] - 1 }),
                    (L = 0),
                    (e.Object = T),
                    (T = null));
                }
              }),
              !1
            );
          d.Solution = !0;
          for (let t = 0; t < J.length; t++) {
            let e = J[t],
              i = e.data('Use'),
              n = e.data('ObjectLetter');
            i.hint ||
              (n.css({ color: m['font-color'], fontWeight: 'bolder', fontStyle: '' }),
              i.img && e.find('img').show(),
              e.data('Correct', !0),
              e.data(et) && e.data(et).css({ opacity: 0 }),
              d.DrawSizedLetter(n, i[it]));
          }
          ((d.Solution = !1), kt());
        },
        pencil: function () {
          if ((kt(), r)) return !1;
          (d.Pencil
            ? (t(this).css({ border: 'solid 1px transparent' }),
              t(this).height(t(this).height() + 2))
            : (t(this).css({ border: 'solid 1px black' }), t(this).height(t(this).height() - 2)),
            (d.Pencil = !d.Pencil));
        },
      },
      RevealWordSearch: function () {
        let t = s.Words[d.IdWord].WordSearch,
          e = V[t];
        if (null != e.Object) return !1;
        (s.Div.find('li#LI' + d.IdWord).addClass('Completed'), s.ResetLi());
        var i = t.split('/'),
          n = i[0].split('-'),
          o = i[1].split('-');
        (gt(n[0] - 1, o[0] - 1),
          (y = { x: n[1] - 1, y: o[1] - 1 }),
          zt({ x: n[1] - 1, y: o[1] - 1 }),
          (L = 0),
          null != e.Object && e.Object.remove(),
          (e.Object = T),
          (e.Input = !1),
          (T = null));
      },
      ProcessHintLetter: function () {
        if (i.isCoded) {
          let t,
            e = d.CodedHint,
            i = S;
          for (O = !0, t = 0; t < e.length; t++)
            ((S = d.Cells[parseInt(e[t].x)][parseInt(e[t].y)]), bt(e[t][it], !1));
          ((O = !1), (S = i));
        }
      },
    };
  }
  function a(t, e, i, n, o) {
    let r = document.createElement('div');
    return (
      r.setAttribute(
        'style',
        'cursor:default;height:' +
          t +
          'px;width:' +
          e +
          'px;background-color:' +
          i +
          '; position: absolute; top:' +
          n +
          'px; left:' +
          o +
          'px;'
      ),
      r
    );
  }
  function s(e, i, n, o, r, l) {
    let s = a(e, i, n, o, r);
    return (t(s).css({ border: 'solid ' + l + ' 1px' }), s);
  }
  function d(e) {
    let i,
      n = new Array(e.find('>*').length),
      o = '';
    return (
      t.each(['b', 'i', 'u', 'sub', 'sup', 'span'], function (o, r) {
        for (i = 0; i < e.children(r).length; i++) {
          let o = e.find(r).eq(i),
            l = o.find('>*').length > 0 ? d(o) : o.text() ? o.text() : '',
            a = t('<div/>')
              .append(t('<' + r + '/>').html(l))
              .html();
          n[e.find('*').index(o)] = null != a ? a : '';
        }
      }),
      t.each(n, function (t, e) {
        o += null != e ? e : '';
      }),
      o
    );
  }
  function c(t) {
    if (null == t) return [];
    var e,
      i,
      n,
      o = t.x.split('-'),
      r = t.y.split('-'),
      l = [],
      a = 1 == o.length ? 'X' : 'Y';
    if ('X' == a)
      for (
        r[0] = parseInt(r[0]),
          r[1] = parseInt(r[1]),
          e = r[0] > r[1] ? r[1] : r[0],
          i = r[0] > r[1] ? r[0] : r[1],
          n = e;
        n <= i;
        n++
      )
        l.push(o[0] + '-' + n);
    if ('Y' == a)
      for (
        o[0] = parseInt(o[0]),
          o[1] = parseInt(o[1]),
          e = o[0] > o[1] ? o[1] : o[0],
          i = o[0] > o[1] ? o[0] : o[1],
          n = e;
        n <= i;
        n++
      )
        l.push(n + '-' + r[0]);
    return l;
  }
  (!(function (t) {
    function e(e, n) {
      return ((e.opts = t.extend({}, t.fn.settings, n)), ((o = e).drawRect = i), o);
      var o;
    }
    function i(t, e, i, o, r) {
      var l = t.opts.stroke;
      (n(t, e, i, o, l), n(t, e + o, i, l, r), n(t, e, i + r, o + l, l), n(t, e, i + l, l, r - l));
    }
    function n(e, i, n, o, r) {
      var l = t(
        '<div style="position:absolute;left:' +
          i +
          'px;top:' +
          n +
          'px;width:' +
          o +
          'px;height:' +
          r +
          'px;clip:rect(0,' +
          o +
          'px,' +
          r +
          'px,0);background-color:' +
          e.opts.color +
          ';overflow:hidden;"></div>'
      );
      return (l.css('opacity', e.opts.alpha), e.append(l), l);
    }
    ((t.fn.settings = { color: '#000000', stroke: 1, alpha: 1 }),
      (t.fn.fillRect = function (i, o, r, l, a) {
        return n(e(t(this), a), i, o, r, l);
      }),
      (t.fn.drawRect = function (i, n, o, r, l) {
        var a = e(t(this), l);
        return (a.drawRect(a, i, n, o, r), t(this));
      }));
  })(jQuery),
    jQuery.fn.extend({
      everyTime: function (t, e, i, n, o) {
        return this.each(function () {
          jQuery.timer.add(this, t, e, i, n, o);
        });
      },
      oneTime: function (t, e, i) {
        return this.each(function () {
          jQuery.timer.add(this, t, e, i, 1);
        });
      },
      stopTime: function (t, e) {
        return this.each(function () {
          jQuery.timer.remove(this, t, e);
        });
      },
    }),
    jQuery.extend({
      timer: {
        guid: 1,
        global: {},
        regex: /^([0-9]+)\s*(.*s)?$/,
        powers: { ms: 1, cs: 10, ds: 100, s: 1e3, das: 1e4, hs: 1e5, ks: 1e6 },
        timeParse: function (t) {
          if (null == t || null == t) return null;
          var e = this.regex.exec(t.toString().trim());
          return e[2] ? parseInt(e[1], 10) * (this.powers[e[2]] || 1) : t;
        },
        add: function (t, e, i, n, o, r) {
          var l = 0;
          if (
            ('function' == typeof i && (o || (o = n), (n = i), (i = e)),
            !('number' != typeof (e = jQuery.timer.timeParse(e)) || isNaN(e) || e <= 0))
          ) {
            (o && o.constructor != Number && ((r = !!o), (o = 0)),
              (o = o || 0),
              (r = r || !1),
              t.$timers || (t.$timers = {}),
              t.$timers[i] || (t.$timers[i] = {}),
              (n.$timerID = n.$timerID || this.guid++));
            var a = function () {
              (r && this.inProgress) ||
                ((this.inProgress = !0),
                ((++l > o && 0 !== o) || !1 === n.call(t, l)) && jQuery.timer.remove(t, i, n),
                (this.inProgress = !1));
            };
            ((a.$timerID = n.$timerID),
              t.$timers[i][n.$timerID] || (t.$timers[i][n.$timerID] = window.setInterval(a, e)),
              this.global[i] || (this.global[i] = []),
              this.global[i].push(t));
          }
        },
        remove: function (t, e, i) {
          var n,
            o = t.$timers;
          if (o) {
            if (e) {
              if (o[e]) {
                if (i)
                  i.$timerID && (window.clearInterval(o[e][i.$timerID]), delete o[e][i.$timerID]);
                else for (var i in o[e]) (window.clearInterval(o[e][i]), delete o[e][i]);
                for (n in o[e]) break;
                n || ((n = null), delete o[e]);
              }
            } else for (e in o) this.remove(t, e, i);
            for (n in o) break;
            n || (t.$timers = null);
          }
        },
      },
    }),
    /MSIE ([0-9]{1,}[\.0-9]{0,})/.exec(navigator.userAgent));
  var h = parseFloat(RegExp.$1),
    u = 'transparent';
  (h &&
    jQuery(window).one('unload', function () {
      var t,
        e,
        n = jQuery.timer.global;
      for (t in n) for (e = n[t], i = e.length; --i; ) jQuery.timer.remove(e[i], t);
    }),
    (t.fn.CrosswordCompiler = function (e, i, l) {
      var a = t(this),
        s = a.attr('id');
      if (null == s) return void alert('You Must Pass An Element With an Id');
      let f = '#' + s,
        g = '@container ' + s + '-frame (max-width:',
        m = t(
          '<style>' +
            f +
            ' td{font-size:auto;vertical-align: middle}' +
            f +
            ' *{-webkit-box-sizing:content-box;-moz-box-sizing:content-box;box-sizing:content-box;margin:0;padding:0;border:0;line-height:normal;text-shadow:none} .ActionButton:active{opacity:0.5} .ButtonTextDiv{width: fit-content !important;}</style>'
        ).appendTo(
          a.css({
            container: s + '-frame / inline-size',
            display: 'flex',
            width: '100%',
            height: 'auto',
            justifyContent: 'inherit',
          })
        ),
        b = t('<div class="CCPuzContainer"></div>')
          .attr('id', s + '-div')
          .css({
            width: '100%',
            height: '100%',
            container: s + '-contain / inline-size',
            display: 'grid',
          })
          .appendTo(a);
      t.isXMLDoc(e) || (e = t.parseXML(e));
      var C,
        x,
        w,
        v,
        y = 0,
        S = 0,
        T = 0,
        E = !1,
        I = 0,
        k = 0,
        L = 0,
        O = ['Software &copy; <span>crossword-compiler.com</span>'],
        z = 0,
        P = 0,
        A = 0,
        R = 'compiler.com',
        M = '',
        W = 0;
      ((_img_start2 =
        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' viewBox='0 0 500 500'%3E%3C"),
        (T = {
          MaxCheat: -1,
          Images: {
            'reveal-word':
              _img_start2 +
              "path d='M3.32,0H496.68A3.34,3.34,0,0,1,500,3.34V496.66a3.34,3.34,0,0,1-3.32,3.34H3.32A3.34,3.34,0,0,1,0,496.66V3.34A3.34,3.34,0,0,1,3.32,0Z' fill-rule='evenodd'/%3E%3Cpath d='M173.8 6.69h150.18v161.08H173.8z' fill='%23fff'/%3E%3Cpath d='M330.62 174.45h162.73v151.09H330.62zm-156.82 0h150.18v151.09H173.8zm-167.15 0h160.5v151.09H6.65z' fill='%230ff'/%3E%3Cpath d='M173.8 332.24h150.18v161.08H173.8z' fill='%23fff'/%3E%3Cpath d='M49.73 289.94l30.46-79.89h11.55l32.33 79.89h-12l-9.18-24.21h-33.4l-8.62 24.21zm22.85-32.8h27.06L91.35 235q-3.73-10.1-5.69-16.68a113.38 113.38 0 0 1-4.38 15.38zm146.31 32.8v-79.89h29.79q9.1 0 14.6 2.42a18.8 18.8 0 0 1 8.6 7.47 19.62 19.62 0 0 1 3.12 10.55 18.26 18.26 0 0 1-2.75 9.63 19.66 19.66 0 0 1-8.32 7.31 20.58 20.58 0 0 1 11.07 7.25 19.42 19.42 0 0 1 3.89 12.09 23.46 23.46 0 0 1-2.37 10.45 20.2 20.2 0 0 1-5.82 7.44 24.55 24.55 0 0 1-8.7 3.94 52.18 52.18 0 0 1-12.83 1.34zm10.53-46.3h17.17c4.66 0 8-.32 10-.93a11.11 11.11 0 0 0 6.05-4 11.57 11.57 0 0 0 2-7 12.82 12.82 0 0 0-1.9-7 9.56 9.56 0 0 0-5.42-4.17q-3.52-1.11-12.07-1.11h-15.83v24.21zm0 36.93h19.78a44.66 44.66 0 0 0 7.17-.39 16.83 16.83 0 0 0 6.07-2.18 11.73 11.73 0 0 0 4-4.46 14 14 0 0 0 1.57-6.75 13.33 13.33 0 0 0-2.29-7.79 12 12 0 0 0-6.33-4.65c-2.68-.89-6.56-1.34-11.61-1.34h-18.36zm207.08-18.65l10.5 2.67q-3.32 13-11.87 19.85-8.55 6.85-21 6.84-12.79 0-20.85-5.26a32.66 32.66 0 0 1-12.21-15.21 54.79 54.79 0 0 1-4.2-21.41q0-12.47 4.73-21.76a32.67 32.67 0 0 1 13.48-14.11 39.06 39.06 0 0 1 19.22-4.82q11.92 0 20 6.1c5.42 4.08 9.19 9.78 11.31 17.15l-10.31 2.45c-1.83-5.8-4.51-10-8-12.68s-7.89-4-13.19-4c-6.08 0-11.19 1.47-15.27 4.41a23.2 23.2 0 0 0-8.53 11.86 47.74 47.74 0 0 0-2.5 15.34 49.05 49.05 0 0 0 2.94 17.77 22.05 22.05 0 0 0 9.15 11.37 25.43 25.43 0 0 0 13.44 3.76 22.45 22.45 0 0 0 14.9-5.12q6.09-5.12 8.26-15.2z' fill-rule='evenodd'/%3E%3C/svg%3E%0A",
            'reveal-letter':
              _img_start2 +
              "path d='M3.32,0H496.68A3.34,3.34,0,0,1,500,3.34V496.66a3.34,3.34,0,0,1-3.32,3.34H3.32A3.34,3.34,0,0,1,0,496.66V3.34A3.34,3.34,0,0,1,3.32,0Z' fill-rule='evenodd'/%3E%3Cpath d='M173.8 6.69h150.18v161.08H173.8zm156.82 167.76h162.73v151.09H330.62z' fill='%23fff'/%3E%3Cpath d='M173.8 174.45h150.18v151.09H173.8z' fill='%23f0f'/%3E%3Cpath d='M6.65 174.45h160.5v151.09H6.65zM173.8 332.24h150.18v161.08H173.8z' fill='%23fff'/%3E%3Cpath d='M253.44 280.11h-18.66l-.07-4.93c0-6.05 1-11 3-15s6-8.3 12-13.21 9.58-8.08 10.75-9.61a12.88 12.88 0 0 0 2.71-7.93 13.19 13.19 0 0 0-4.8-10.24q-4.78-4.28-12.91-4.28a19.65 19.65 0 0 0-13.11 4.48q-5.26 4.5-7.24 13.69l-18.81-2.4c.55-8.79 4.26-16.22 11.15-22.35s15.94-9.19 27.14-9.19q17.69 0 28.13 9.29 10.44 9.29 10.45 21.6a23.81 23.81 0 0 1-3.86 12.97q-3.84 6.09-16.39 16.6c-4.33 3.6-7 6.53-8.06 8.73s-1.52 6.13-1.42 11.81zm-18.66 27.63v-20.57h18.66v20.57z' fill-rule='evenodd'/%3E%3C/svg%3E%0A",
            revert:
              _img_start2 +
              "defs%3E%3ClinearGradient id='A' x1='250.27' y1='442.5' x2='250.27' y2='-61.19' gradientUnits='userSpaceOnUse'%3E%3Cstop offset='0' stop-color='%2372bef0'/%3E%3Cstop offset='.03' stop-color='%2357abe4'/%3E%3Cstop offset='.07' stop-color='%233994d6'/%3E%3Cstop offset='.12' stop-color='%232182cb'/%3E%3Cstop offset='.17' stop-color='%230f76c3'/%3E%3Cstop offset='.22' stop-color='%23056ebe'/%3E%3Cstop offset='.28' stop-color='%23026cbd'/%3E%3Cstop offset='.39' stop-color='%230971c0'/%3E%3Cstop offset='.55' stop-color='%231b7ec8'/%3E%3Cstop offset='.73' stop-color='%233994d6'/%3E%3Cstop offset='.94' stop-color='%2363b3e9'/%3E%3Cstop offset='1' stop-color='%2372bef0'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cg fill-rule='evenodd'%3E%3Cpath d='M272.7,8.5,99.18,123.67,270,229l.8-66.25a122.29,122.29,0,1,1-143,126.39h-86C44.93,401.43,136.93,491.5,250,491.5c115,0,208.23-93.23,208.23-208.23,0-107.59-81.62-196.11-186.31-207.07Z' fill='%23026cbd'/%3E%3Cpath d='M262.56,27.13l-145,96.23,142.76,88,.73-60.36,11.46,2A132.2,132.2,0,1,1,118.7,299.07H52.27C60.33,401.51,146.07,481.59,250,481.59c109.52,0,198.31-88.79,198.31-198.32,0-101.37-76.65-186.66-177.42-197.21l-9-.94Z' fill='url(%23A)'/%3E%3Cpath d='M262.56 27.13l-145 96.23 6.6 4.07 138.29-91.78.11-8.52zm119.44 249q.19 3.56.2 7.14a132.2 132.2 0 0 1-263.45 15.8H52.27l.8 8h66.3A132.2 132.2 0 0 0 382 276.13zm65.92-5.43c-9.55-92.13-82.48-166.81-176.35-176.64l-9-.94.1-7.92 8.23.86c96.53 10.11 170.94 88.87 176.97 184.64z' fill='%23fff' opacity='.53'/%3E%3C/g%3E%3C/svg%3E%0A",
            solution:
              _img_start2 +
              "path d='M287.2,362.89H207.71c-.22-11.45-.32-18.34-.32-20.88q0-38.49,12.83-63.39t51-56q38.32-31,45.79-40.7a54.27,54.27,0,0,0,11.56-33.6c0-16.86-6.79-31.38-20.46-43.36s-31.91-18.12-55-18.12c-22.26,0-40.81,6.36-55.87,19s-25.22,32-30.84,58L86.23,153.65Q89.74,97.84,133.72,59t115.64-38.9q75.38,0,119.89,39.32t44.52,91.48c0,19.19-5.41,37.52-16.33,54.7s-34.13,40.59-69.85,70.27c-18.44,15.27-29.89,27.67-34.34,37s-6.47,26-6.05,50Zm-79.49,117V392.78H287.2v87.13Z' fill='%234697bf' fill-rule='evenodd'/%3E%3C/svg%3E%0A",
            check:
              _img_start2 +
              "defs%3E%3ClinearGradient id='A' x1='218' y1='2.34' x2='209' y2='359.34' gradientUnits='userSpaceOnUse'%3E%3Cstop offset='.26'/%3E%3Cstop offset='.32' stop-color='%230b0b0b'/%3E%3Cstop offset='.44' stop-color='%23292929'/%3E%3Cstop offset='.59' stop-color='%235a5a5a'/%3E%3Cstop offset='.77' stop-color='%239e9e9e'/%3E%3Cstop offset='.97' stop-color='%23f3f3f3'/%3E%3Cstop offset='1' stop-color='%23fff'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cg fill-rule='evenodd'%3E%3Cpath d='M79.51,80.39,59.05,152.73h41.66L79.51,80.39ZM65.06,43H96.23l59.62,188H123.13l-12.82-44.77H49.55L37.08,231H5.89L65.06,43ZM195,76.8v43.46h43c6.66,0,11.56-1.78,14.64-5.32s4.68-9,4.68-16.4-1.56-13-4.68-16.5-8-5.24-14.64-5.24Zm43.5,121c6.72,0,11.59-1.79,14.64-5.33s4.58-9.07,4.58-16.66-1.53-13.31-4.61-16.89-8-5.36-14.61-5.36H195v44.24ZM242.62,231h-77V43h71.84c9.09,0,16.46.7,22.1,2a32.71,32.71,0,0,1,13.77,6.51,41.61,41.61,0,0,1,11.75,16.88,64.41,64.41,0,0,1,4,23.52c0,10.52-1.68,19.37-5,26.66A45.31,45.31,0,0,1,268.3,137a38.44,38.44,0,0,1,16,16.54c3.47,7,5.19,15.66,5.19,26.18,0,17.54-3.79,30.5-11.42,38.79S258.66,231,242.62,231ZM370.32,75.24q-18.26,0-26.29,15.57T336,142q0,31,7.7,43.59t26.61,12.65h48.27V231h-49.7c-11,0-19.57-1.27-25.87-3.76a49.3,49.3,0,0,1-17.65-12.74q-10.77-11.52-16.14-30t-5.35-44.19q0-49.87,16.06-73.57T369.73,43h48.86V75.24Z' fill='url(%23A)'/%3E%3Cpath d='M36.29 298.31l64.21-64.22 129.49 129.49 196.18-196.17 65.27 61.74-263.21 263.22L36.29 298.31z' fill='%23279b2c'/%3E%3C/g%3E%3C/svg%3E%0A",
            pencil:
              _img_start2 +
              "defs%3E%3ClinearGradient id='A' x1='258.186' y1='234.733' x2='259.511' y2='197.022' gradientUnits='userSpaceOnUse'%3E%3Cstop offset='.15' stop-color='%23e8b11f'/%3E%3Cstop offset='1' stop-color='%23f4c668'/%3E%3C/linearGradient%3E%3ClinearGradient id='B' x1='330.4' y1='262.72' x2='274.55' y2='226.42' xlink:href='%23A'/%3E%3ClinearGradient id='C' x1='235.28' y1='203.08' x2='189.2' y2='154.21' xlink:href='%23A'/%3E%3CradialGradient id='D' cx='316' cy='128.38' r='88.17' gradientTransform='translate(244.03 -205.03) rotate(55.71)' gradientUnits='userSpaceOnUse'%3E%3Cstop offset='.31' stop-color='%23e3e3e3'/%3E%3Cstop offset='.55' stop-color='%23dcdcdc'/%3E%3Cstop offset='.88' stop-color='%23cacaca'/%3E%3Cstop offset='1' stop-color='%23c2c2c2'/%3E%3C/radialGradient%3E%3ClinearGradient id='E' x1='85.74' y1='390.04' x2='233.75' y2='465.44' gradientUnits='userSpaceOnUse'%3E%3Cstop offset='0' stop-color='%23f0d5a3'/%3E%3Cstop offset='.2' stop-color='%23f1d7a7'/%3E%3Cstop offset='.41' stop-color='%23f3ddb4'/%3E%3Cstop offset='.63' stop-color='%23f6e7ca'/%3E%3Cstop offset='.86' stop-color='%23fbf4e8'/%3E%3Cstop offset='1' stop-color='%23fff'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cpath transform='matrix(.563382 -.826197 .826197 .563382 -64.75 307.84)' d='M73.22 188.55h371.33v53.26H73.22z' fill='url(%23A)'/%3E%3Cg fill-rule='evenodd'%3E%3Cpath d='M385.49,76.8,176.29,383.58,198,398.35c11.16,7.62,31.16,7.88,38.78-3.28l181.52-266.2a24.62,24.62,0,0,0-6.45-34.13Z' fill='url(%23B)'/%3E%3Cpath d='M132.28 353.57l209.2-306.78-29.14-19.88a24.64 24.64 0 0 0-34.13 6.46L96.68 299.57c-7.61 11.16 2.8 31.63 14 39.25z' fill='url(%23C)'/%3E%3Cpath d='M254.5,68.14l140.05,95.5,23.7-34.77a24.62,24.62,0,0,0-6.45-34.13L312.34,26.91a24.64,24.64,0,0,0-34.13,6.46Z' fill='%23981111'/%3E%3C/g%3E%3Cpath transform='matrix(.563382 -.826197 .826197 .563382 31.9 317.13)' d='M300.88 43.63h30.25v169.51h-30.25z' fill='url(%23D)'/%3E%3Cg fill-rule='evenodd'%3E%3Cpath d='M77.5,477.06Q86,390.19,94.58,303.33A454.47,454.47,0,0,0,234,398.4Z' fill='url(%23E)'/%3E%3Cpath d='M84.73 408.36l-6.83 69 63-31.6c-17.67-21.3-37.05-34.01-56.17-37.4z'/%3E%3C/g%3E%3C/svg%3E%0A",
            submit:
              _img_start2 +
              "defs%3E%3ClinearGradient id='A' x1='73.43' y1='240.4' x2='416.73' y2='240.4' gradientUnits='userSpaceOnUse'%3E%3Cstop offset='0' stop-color='%2394adcf'/%3E%3Cstop offset='1' stop-color='%233465a4'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cg fill-rule='evenodd'%3E%3Cpath d='M246.33 250c-24.94 1.17-52.09 7.58-73.54 19.69-24.14 13.62-40.08 33.92-41.09 62.4v4.08c.3 30.83 10.36 59.23 31.02 82.43s70.92 52.51 98.13 71.17c-68.2-17.31-120.71-25.39-168.9-84.2-21-25.66-34-55.95-37.16-89a176.08 176.08 0 0 1 14-86.47c10.28-23.72 26-45.89 46-62.33 23.7-19.42 51.11-33 80.59-41.16a253.39 253.39 0 0 1 50.62-8.48l-.25-107.9L446 182.59 246.61 365.25z' fill='%23204a87'/%3E%3Cpath d='M263.55 38.1l168.09 144.71-175.56 160.85-.24-103.4H253c-26.41.26-58.81 6.42-84.85 21.11-25.43 14.36-44.74 37-45.92 70.47l-.05 4.29c.81 82.87 51.42 107.25 111.49 140.49-53.94-17.44-94.84-28.92-134.3-77.08-21.44-26.17-32.27-55.19-35-83.9a166.35 166.35 0 0 1 13.26-81.76c10.21-23.58 25.39-44.06 43.31-58.75 25.09-20.56 52.29-32.51 77.08-39.34a245.14 245.14 0 0 1 57.65-8.57L255.34 31l8.21 7.07zm153.18 145L265.28 52.68l.2 84.3h-4.94a235.14 235.14 0 0 0-60 8.3 198.28 198.28 0 0 0-73.44 37.48c-16.76 13.74-31 32.91-40.53 55a156.54 156.54 0 0 0-12.47 76.92c2.59 26.83 12.76 54 32.87 78.55a185 185 0 0 0 38.43 34.86c-16.8-20.05-32.77-50.05-33.18-91.91l.06-4.7c1.32-37.54 22.75-62.81 51-78.74 27.62-15.59 61.82-22.12 89.62-22.4l8.06.1 4.76.17.21 90.6z' fill='%2394adcf'/%3E%3Cpath d='M416.73 183.07L265.28 52.68l.2 84.3h-4.94a235.14 235.14 0 0 0-60 8.3 198.28 198.28 0 0 0-73.44 37.48c-16.76 13.74-31 32.91-40.53 55a156.54 156.54 0 0 0-12.47 76.92c2.59 26.83 12.76 54 32.87 78.55a185 185 0 0 0 38.43 34.86c-16.8-20.05-32.77-50.05-33.18-91.91l.06-4.7c1.32-37.54 22.75-62.81 51-78.74 27.62-15.59 61.82-22.12 89.62-22.4l8.06.1 4.76.17.21 90.6z' fill='url(%23A)'/%3E%3Cpath d='M269.9,56.66c28.54,57.5,50.74,123.23,59.56,206.36l87.27-79.95Z' fill='%233465a4'/%3E%3C/g%3E%3C/svg%3E%0A",
            save:
              _img_start2 +
              "defs%3E%3ClinearGradient id='A' x1='249.13' y1='23.67' x2='252.13' y2='800.67' gradientUnits='userSpaceOnUse'%3E%3Cstop offset='.32' stop-color='%23201f25'/%3E%3Cstop offset='1' stop-color='%23fff'/%3E%3C/linearGradient%3E%3ClinearGradient id='B' x1='243.53' y1='528.32' x2='249.53' y2='147.32' xlink:href='%23A'/%3E%3ClinearGradient id='C' x1='258.08' y1='122.76' x2='261.09' y2='524.76' xlink:href='%23A'/%3E%3Cpath id='D' d='M75.55 243.75a6.61 6.61 0 1 1-6.77 6.61 6.69 6.69 0 0 1 6.77-6.61z'/%3E%3Cpath id='E' d='M26.76 31.55a9.36 9.36 0 1 1-9.6 9.36 9.48 9.48 0 0 1 9.6-9.36z'/%3E%3C/defs%3E%3Cg fill-rule='evenodd'%3E%3Cpath d='M0 0h500v455.16l-44.38 43.29H0V0z' fill='url(%23A)'/%3E%3Cpath d='M72.81,14H426.56a10.2,10.2,0,0,1,10.29,10V251.11a10.2,10.2,0,0,1-10.29,10H72.81a10.2,10.2,0,0,1-10.29-10V24A10.2,10.2,0,0,1,72.81,14Z' fill='url(%23B)'/%3E%3Cpath d='M92.51 162.66a3.7 3.7 0 1 1 0-7.39H405.1a3.7 3.7 0 1 1 0 7.39zm0-76.15a3.7 3.7 0 1 1 0-7.4H405.1a3.7 3.7 0 1 1 0 7.4zm0 122.68a3.7 3.7 0 1 1 0-7.39H405.1a3.7 3.7 0 1 1 0 7.39z' fill='%23b3b3b3'/%3E%3C/g%3E%3Cpath d='M62.52 37.4h374.33v7.39H62.52z' fill='%23b3b3b3'/%3E%3Cg fill-rule='evenodd'%3E%3Cpath d='M62.52,37.4H436.85V24a10.2,10.2,0,0,0-10.29-10H72.81A10.2,10.2,0,0,0,62.52,24Z' fill='%23919096'/%3E%3Cuse xlink:href='%23D'/%3E%3Cuse xlink:href='%23D' x='345.45'/%3E%3Cg fill='%23fff'%3E%3Cuse xlink:href='%23E'/%3E%3Cuse xlink:href='%23E' x='442.3'/%3E%3C/g%3E%3Cpath d='M394.14 301.48H83.6c-12.57 0-22.85 10-22.85 22.29v174.68H417V323.77c0-12.26-10.29-22.29-22.86-22.29z' fill='%237f7f81'/%3E%3Cpath d='M387 313.15H92.42c-11.93 0-21.68 9.51-21.68 21.14V500h338V334.29c-.05-11.63-9.8-21.14-21.74-21.14z'/%3E%3Cpath d='M124.49,500H396.13V341.82c0-11.63-7.83-21.14-17.42-21.14H141.91c-9.59,0-17.42,9.51-17.42,21.14Z' fill='url(%23C)'/%3E%3C/g%3E%3Cpath d='M305.63 331.83h43.16v132.91h-43.16z'/%3E%3C/svg%3E%0A",
          },
          TimerObject: { Enabled: !1, OnLoad: !1, Start: 0, Pause: !0, Stop: !0, Actions: !1 },
          ClueHintPanel: 0,
          TimerDiv: '',
          DivTitle: '',
          Cells: {},
          Words: {},
          Alphabet: [],
          LetterAlphabet: [],
          XMLGame: {},
          Timer: { 'initial-value': 0, 'start-on-load': 'false', 'allow-pause': 'true' },
          XML: {},
          Responsive: l.RESPONSIVE ?? !0,
          HintTextDefault: l.HINTDEFAULTHTML || '',
          MinScale: l.MINSCALE || 0.7,
          Width: 0,
          Height: 0,
          Params: {},
          Attributes: {
            'background-color': 'white',
            'wrong-letter-color': '',
            'selected-cells-color': 'gray',
            'cursor-color': 'yellow',
            width: 0,
            height: 0,
            'scroll-width': 0,
            'scroll-height': 0,
            'hide-numbers': !1,
            'show-alphabet': !1,
            'enforce-alphabet': !1,
            'validate-sudoku': !0,
            'title-left': !1,
            'title-height': 11,
            'type-skip-existing': !1,
            'clue-float-background': '#CCFFFF',
            'pencil-color': '#00FF00',
          },
          RunTimer: function () {
            let e = T.TimerObject;
            'object' == typeof T.TimerDiv &&
              e.Stop &&
              e.Enabled &&
              ((e.Stop = !1),
              T.TimerDiv.fadeTo('fast', 1).everyTime(1e3, function () {
                T.TimerObject.Start++;
                let i = Math.floor(e.Start / 60),
                  n = e.Start % 60;
                ((i = i < 10 ? '0' + i : i), (n = n < 10 ? '0' + n : n), t(this).html(i + ':' + n));
              }));
          },
          RespaceClues: function () {
            let e = S.Attributes,
              i = S.Div,
              n = 'below' == e.layout,
              o = parseInt(e.width),
              r = i.find('li');
            if (n)
              i.css({ width: y.ViewWidth, height: o }).children('div').css({
                marginLeft: 0,
                width: '50%',
                display: 'inline-block',
                marginTop: 0,
                height: o,
              });
            else if (null != i) {
              i.css('left' == e.layout ? 'margin-right' : 'margin-left', e.gutter + 'px');
              let t = i.children('div');
              t.css({ height: y.ViewHeight / t.length });
            }
            (t.each(r, function () {
              if (1 == t(this).find('>span').eq(0).length) {
                let e = t(this),
                  i = e.width() - e.find('>span').eq(0).width(),
                  n = e.find('>p').eq(0),
                  o = n.find('span'),
                  r = 1 == o.eq(0).length ? o.eq(0).width() : 0,
                  l = o.eq(1);
                (e.find('>span').eq(0).css({ marginLeft: i }),
                  n.css({ width: i - 2 }),
                  l.css({ width: i - r }),
                  l.width() != i - r &&
                    (l.html(l.html() + '&nbsp;&nbsp;&nbsp;'), l.css({ width: i - r - 2 })));
              }
            }),
              'true' == e['right-align-numbers'] &&
                t.each(r, function () {
                  let e,
                    i,
                    n = t(this).find('p'),
                    o = 1 == n.find('>span').eq(0).length ? n.find('>span').eq(0) : null,
                    r = 1 == n.find('>span').eq(1).length ? n.find('>span').eq(1) : null;
                  if (
                    null != o &&
                    null != r &&
                    ((e = parseInt(o.parent().width() / 10)), o.height() != r.height())
                  ) {
                    if (
                      (r.css({ position: 'absolute' }),
                      h >= 8 && h < 9 && r.css({ marginRight: '16px' }),
                      o.width() - 10 > e)
                    )
                      for (
                        i = o.width() - e,
                          p = t('<span/>'),
                          span = t('<span/>').html(r.html()),
                          r.html('&nbsp;').append(p).append(span),
                          r.css({ left: e - 1 + 'px' });
                        p.width() < i;

                      )
                        p.html(p.html() + '&nbsp;');
                    r.parent().css({ height: r.height() });
                  }
                }),
              i.children('div').each(function () {
                let e = t(this);
                (e.find('p').eq(0).remove(),
                  e.find('div:eq(0)').height() + e.find('*:eq(0)').height() > e.height() &&
                    e.find('div:eq(0)').height(e.height() - e.find('*:eq(0)').height()),
                  navigator.userAgent.indexOf('Mozilla') >= 0 &&
                    e.find('li:last').css({ marginBottom: '1px' }));
              }));
          },
        }),
        (T.Iframe = b),
        (y = r(T, b)),
        (S = n(T, y, b)),
        (C = o(T, y, b, S)),
        (T.Grid = y),
        (T.Clues = S),
        (T.PuzzleState = C),
        (T.Params = l),
        null != i && (T.images = t.extend(T.Images, i)),
        (T.XmlDoc = e),
        (T.XML = t(e)),
        (z = t(e).find('rectangular-puzzle')),
        (T.XMLRect = z),
        t.each(['crossword', 'coded', 'sudoku', 'word-search'], function (t, e) {
          1 == z.find(e).length &&
            ((T.XMLGame = z.find(e)),
            (T.isWordSearch = 'word-search' == e),
            (T.isSudoku = 'sudoku' == e),
            (T.isCoded = 'coded' == e));
        }),
        (function () {
          ((I = T.XML.find('applet-settings')),
            (A = T.Attributes),
            (T.AppletSettings = I),
            t.each(A, function (t, e) {
              let i = I.attr(t);
              null != i &&
                (!1 === A[t] ? (i = 'true' == i) : 0 === A[t] && (i = parseInt(i)), (A[t] = i));
            }));
          let e = I.find('timer'),
            i = I.find('completion');
          (1 == i.length && i.attr('cheating') && (T.MaxCheat = parseInt(i.attr('cheating'))),
            1 == e.length &&
              ((T.TimerObject.Enabled = !0),
              e.attr('initial-value') && (T.TimerObject.Start = parseInt(e.attr('initial-value'))),
              e.attr('start-on-load') && (T.TimerObject.OnLoad = 'true' == e.attr('start-on-load')),
              e.attr('allow-pause') && (T.TimerObject.Pause = 'true' == e.attr('allow-pause'))),
            (function () {
              let e = I.find('copyright'),
                i = T.Params,
                n = i.TITLEHEIGHT,
                o = i.MAXCHEATS,
                r = l.ROOTIMAGES || 'CrosswordImages/';
              function a(t, e) {
                l.hasOwnProperty(t) && (A[e] = l[t]);
              }
              ((v = i.BUSINESS || 0),
                (x = v || 2424),
                (w = i.CL || 0),
                t.each(T.Images, function (t, e) {
                  e.indexOf('data:image') < 0
                    ? (T.Images[t] = r + e)
                    : (T.Images[t] = '"' + e + '"');
                }),
                n && parseInt(n) && (A['title-height'] = parsetInt(n)));
              o && parseInt(o) && (T.MaxCheat = parseInt(o));
              let s = 'SCROLLWIDTH',
                c = 'SCROLLHEIGHT';
              l.hasOwnProperty(s) && (A['scroll-width'] = parseInt(l[s]) || 0);
              l.hasOwnProperty(c) && (A['scroll-height'] = parseInt(l[c]) || 0);
              (a('TITLELEFT', 'title-left'),
                a('CURCOLOR', 'cursor-color'),
                a('WRONGCOLOR', 'wrong-letter-color'),
                a('BACKCOLOR', 'background-color'),
                a('VALIDATESUDOKU', 'validate-sudoku'),
                l.hasOwnProperty('TIMER') && (T.Timer.Enabled = l.TIMER));
              l.hasOwnProperty('STARTTIME') && (T.Timer.Start = l.STARTTIME);
              l.hasOwnProperty('NOPAUSE') && (T.Timer.Pause = l.NOPAUSE);
              l.hasOwnProperty('TIMEFROMLOAD') && (T.Timer.OnLoad = l.TIMEFROMLOAD);
              ((P = l.COPYRIGHT || (1 == e.length ? ('' == d(e) ? e.text() : d(e)) : '')),
                270428 === x
                  ? (P = '&copy; www.crossworldcommunication.com')
                  : v && 11 * (v + 208) != w && (x = 0));
            })());
        })(),
        b.css({
          backgroundColor: A['background-color'] + '',
          width: A.width + '',
          height: A.height + '',
          position: 'relative',
          '-webkit-user-select': 'none',
          '-moz-user-select': 'none',
          '-webkit-touch-callout': 'none',
          '-webkit-tap-highlight-color': 'transparent',
        }),
        (function () {
          let e = I.find('title'),
            i = e.length > 0 ? (d(e) ? d(e) : e.text()) : '';
          ((i = l.hasOwnProperty('TITLE') ? T.Params.TITLE : i),
            null != i &&
              '' != i &&
              '%TITLE%' != i &&
              (T.DivTitle = t('<div />')
                .css({
                  fontSize: A['title-height'] + 'px',
                  width: '100%',
                  textAlign: A['title-left'] ? 'left' : 'center',
                  fontFamily: 'sans-serif',
                  fontWeight: 'normal',
                  gridArea: 'title',
                })
                .addClass('PuzzleTitle')
                .html(i)
                .appendTo(b)));
        })(),
        1 == T.TimerObject.Enabled &&
          (T.TimerDiv = t('<div/>')
            .css({
              fontFamily: 'sans-serif',
              fontSize: '14px',
              fontWeight: 'bolder',
              cursor: 'default',
            })
            .addClass('Timer')
            .html('00:00')
            .on('click', function () {
              1 == T.TimerObject.Pause &&
                (t(this).stopTime(), t(this).fadeTo('fast', 0.5), (T.TimerObject.Stop = !0));
            })),
        (function () {
          let e = [],
            i = I.find('actions'),
            n = i.attr('buttons-layout'),
            o = 'true' == i.attr('wide-buttons');
          if (
            ((E = 'below' == n),
            (W = 'true' == i.attr('graphical-buttons')),
            (M = t('<div/>')
              .css({
                fontSize: A['title-height'] + 'px',
                fontWeight: 'normal',
                fontFamily: 'sans-serif',
                display: 'flex',
                gridArea: 'action',
                flexDirection: E ? 'row' : 'column',
                gap: '4px',
              })
              .addClass('CCPuzButtons')),
            W && m.append('.ActionButton.Graphical{margin-top:3px !important}'),
            t.each(y.ButtonActions, function (n, o) {
              let r,
                l,
                a = i.find(n),
                s = 35,
                d = 'pencil' == n;
              1 == a.length &&
                (!W && E && (s = 30),
                (r = t('<div/>')
                  .data('id', n)
                  .css({ height: s, cursor: 'pointer', textAlign: 'left' })),
                d || r.attr('role', 'button'),
                W
                  ? (r
                      .append(
                        t('<div/>')
                          .addClass(n + ' ButtonImage')
                          .attr('aria-hidden', 'true')
                      )
                      .addClass('ActionButton Graphical')
                      .on('click', o),
                    m.append(
                      '.' +
                        n +
                        '{height:25px;width:25px;vertical-align:middle;background:url(' +
                        T.Images[n] +
                        ') no-repeat;background-size: 25px;}' +
                        (-1 !== T.Images[n].indexOf('.png')
                          ? '@media (-webkit-min-device-pixel-ratio: 2),(min-resolution:2dppx),(min-resolution: 120dpi) {.' +
                            n +
                            '{background:url(' +
                            T.Images[n].replace('.png', '_2x.png') +
                            ');background-size: 25px 25px;}}'
                          : '')
                    ))
                  : d
                    ? t("<input type='checkbox' />")
                        .appendTo(r)
                        .css({ 'margin-right': '4px', 'vertical-align': 'middle' })
                        .on('click', o)
                    : r.on('click', o).addClass('ActionButton'),
                (l = t('<span>')
                  .addClass('ButtonText')
                  .css({ lineHeight: s + 'px', whiteSpace: 'nowrap', marginLeft: W ? '2px' : 0 })
                  .html(a.attr('label'))),
                e.push(l),
                r.append(
                  t('<div/>').append(l).addClass('ButtonTextDiv').css('width', 'fit-content')
                ),
                W ||
                  r.css({
                    backgroundColor: d ? '' : '#E0E0E0',
                    textAlign: d ? 'left' : 'center',
                    marginBottom: '2px',
                    border: 'pencil' != n ? 'solid gray 1px' : 'solid 0px',
                  }),
                r.appendTo(M).find('*').css('display', 'inline-block'));
            }),
            0 != e.length)
          )
            if (E) {
              (M.css({
                width: 'fit-content',
                margin: 'auto',
                display: 'flex',
                flexWrap: 'wrap',
                flexDirection: 'row',
                justifyContent: 'center',
                height: 35,
              }).appendTo(b),
                e.forEach(function (t) {
                  let e = W ? 35 : 4,
                    i = t.parent(),
                    n = i.parent(),
                    o = t.width() + 4;
                  (W || (n.find('>input').length > 0 ? (e = 25) : o < 70 && (o = 70)),
                    i.width(o),
                    (o += e),
                    n.css({ display: 'inline-block', width: W ? 'fit-content' : o + 'px' }));
                }),
                T.Responsive &&
                  W &&
                  m.append(
                    '@container ' + s + '-contain (max-width:',
                    1.05 * +M.width() +
                      'px){.ButtonText{display: none !important;}div.ActionButton{padding-left: 5px !important;padding-right: 5px !important;}}'
                  ));
              let t = M.width(),
                i = parseInt(A.width) / t;
              i < 1 &&
                (M.css({ transform: 'scale(' + i + ')', transformOrigin: 'left' }), M.width(t / i));
            } else
              (M.css({ width: o && W ? 100 : W || o ? 80 : 60 }).appendTo(b),
                e.forEach(function (t) {
                  let e = t.width(),
                    i = t.parent().width();
                  e > i && t.css({ fontSize: ((parseFloat(t.css('font-size')) * i) / e) * 0.95 });
                }),
                'left' == n && (M.css('margin-right', '5px'), (T.TimerObject.Actions = !0)));
          else E = !0;
        })(),
        S.Start(t(e)),
        y.Start(t(e)),
        (function () {
          let e = z.attr('alphabet');
          if ((null != e && (T.Alphabet = e.split('')), A['show-alphabet'])) {
            let i = 14,
              n = 14,
              o = 0;
            for (e = T.Alphabet; i * e.length > y.ViewWidth - 2; ) (i--, n--);
            ((o += (y.ViewWidth - e.length * i) / 2),
              m.append(
                '.CCPuzAlphabet {display:flex;justify-content:space-between;grid-area:alph;align-items:center;width: ' +
                  e.length * i +
                  'px;background-color:white;font-family:sans-serif}.AlphabetLetter {text-align: center;font-weight: bolder;font-size: ' +
                  n +
                  'px;cursor: pointer;height: 20px;flex: 1;align-items: center;justify-content: center;}'
              ),
              (L = t('<div class="CCPuzAlphabet"/>')
                .appendTo(b)
                .css({ marginLeft: o, marginTop: 2, marginBottom: 1 })),
              t.each(e, function (e, i) {
                T.LetterAlphabet.push(
                  t('<div class="AlphabetLetter">' + i + '</div>')
                    .appendTo(L)
                    .on('click', function () {
                      y.CellSelected() && y.DrawLetter(t(this).html(), 5e3);
                    })
                );
              }));
          }
        })(),
        S.KeyWord(),
        (T.Words = S.Words),
        (T.Cells = y.Cells),
        T.isWordSearch ||
          t.each(T.Words, function (e, i) {
            if ('true' == i.keyword) return;
            let n = b.find('li#LI' + e);
            (t.each(i.Squares, function (t, o) {
              let r = o.split('-'),
                l = T.Cells[parseInt(r[0])][parseInt(r[1])];
              (l.data('WordId').push(e), l.data('WordItem').push(i), l.data('LIS').push(n));
            }),
              t.each(i.cells, function () {
                let i = t(this),
                  o = c({ x: i.attr('x'), y: i.attr('y') });
                t.each(o, function (t, i) {
                  let o = i.split('-'),
                    r = T.Cells[parseInt(o[0])][parseInt(o[1])];
                  null != r &&
                    (r.data('ImLink', !0), r.data('WordId').push(e), r.data('LIS').push(n));
                });
              }));
          }),
        S.SetEventClick(),
        C.SetUrl(),
        y.LoadProgress());
      let H = 'true' == y.Settings['thick-border'],
        D = window.visualViewport,
        U = y.ViewWidth,
        F = y.ViewHeight,
        j = '' != y.Settings['numbered-sides'].top,
        G = S.Attributes,
        q = G.layout,
        B = 'left' == q,
        _ = E ? (B ? 'clues' : '.') : 'action',
        N = B ? '.' : 'right' == q ? 'clues' : '.',
        V = E ? '.' : 'action',
        X =
          (T.DivTitle ? '". title ." ' : '') +
          `". cluehint ." "${_} grid ${N}" "${V} copy copy"` +
          (T.Clues.HasKeyWord ? '". keyword keyword"' : '') +
          (L ? ` "${V} alph ."` : '') +
          (E ? (B ? ' "action action ."' : ' ". action action"') : '') +
          ('below' == q ? `"${V} clues ."` : ''),
        $ = H ? 3 : 0,
        K = y.Size;
      if (
        (j &&
          !y.Scroll &&
          (E || M.css({ marginTop: K }),
          S.Div && S.Div.css({ marginTop: K }),
          (F += K),
          (U += K),
          ($ += K)),
        $ && y.Div.css({ transform: 'translate(' + $ + 'px,' + $ + 'px)' }),
        y.Div.css({ height: F, width: U }),
        m.append(
          f +
            '-div{max-width:' +
            (A.width + 2) +
            `px;height:auto;grid-template-columns: min-content ${U}px min-content;grid-template-areas:` +
            X +
            '}'
        ),
        S.Div &&
          (function (e) {
            let i = parseInt(e['font-size']);
            (t('head').append(
              '<style type="text/css">.ClueHint{background-color:' +
                A['clue-float-background'] +
                ';font-family:' +
                e['font-family'] +
                '}</style>'
            ),
              T.Responsive &&
                (T.ClueHintPanel = t(
                  "<div class='Clues ClueHintPanel ClueHint' aria-hidden='true'></div>"
                )
                  .css({
                    border: 'solid 1px black',
                    padding: '2px',
                    paddingRight: '8px',
                    gridArea: 'cluehint',
                    minHeight: 2 * i + 5,
                    alignItems: 'center',
                    lineHeight: 1.1,
                    display: 'none',
                    fontSize: i,
                  })
                  .appendTo(b)
                  .html(T.HintTextDefault)));
          })(G),
        T.Responsive)
      ) {
        if (
          S.Div &&
          (j && T.ClueHintPanel && T.ClueHintPanel.css('margin-left', K),
          'below' != q && !T.isWordSearch)
        ) {
          let t = A.width - parseInt(G.width);
          m.append(
            g +
              (A.width - 4) +
              'px) {' +
              f +
              '-div{max-width:' +
              t +
              'px;}#CluesPanel {display: none !important;} .ClueHintPanel{display: grid !important}.Timer {font-size:11px !important}}'
          );
        }
        if (!E) {
          let t = T.isWordSearch && 'below' != q ? parseInt(G.width) : 0,
            e =
              '.CCPuzButtons{flex-direction:row !important;width:auto !important;margin-top:3px !important;flex-wrap:wrap;justify-content:center}.Timer{line-height:31px !important} ' +
              f +
              '-div{grid-template-areas:' +
              X.replace(/action/g, '.') +
              ' ". action .";max-width:' +
              (y.ViewWidth + 1) +
              'px}',
            i = U + 40 + t;
          (m.append(
            g +
              (U + M.width() + t) +
              'px){' +
              (W
                ? '.ButtonText{display: none !important}.CCPuzButtons{width:auto !important}.Timer{padding:2px !important}div.ActionButton{padding-left: 3px !important;padding-right: 3px !important;}' +
                  f +
                  '-div{max-width:' +
                  i +
                  'px}}'
                : e +
                  '.ButtonTextDiv{min-width:60px;padding:2px !important}.ButtonText{line-height:31px !important}' +
                  f +
                  '-div{min-width:' +
                  (i - 40) +
                  'px}}')
          ),
            W && m.append(g + i + 'px){' + e + '}'));
        }
        if (D) {
          let t = U + (S.Div && T.isWordSearch && 'below' != q ? S.Div.width() : 0),
            e = t,
            i = Math.min(D.width, a.width()) / t,
            n = 'center' == window.getComputedStyle(a[0], null).getPropertyValue('justify-content');
          if (
            (i > T.MinScale && i < 1
              ? ((e = D.width / i), (i *= 0.98))
              : !y.Scroll && i < T.MinScale
                ? ((i = 1), a.css({ overflow: 'auto', justifyContent: 'left' }))
                : (i = T.MinScale),
            1 != i)
          ) {
            let o = (i + 1) / 2,
              r =
                g +
                'Xpx) {' +
                f +
                '-div{transform: scale(Y);transform-origin: ' +
                (n ? 'center' : 'left') +
                ' top;min-width:' +
                t +
                'px !important}}';
            (i == T.MinScale && (m.append(r.replace('X', e - 4).replace('Y', o)), (e = t * o)),
              m.append(r.replace('X', e - 4).replace('Y', i)));
          }
        }
      }
      (b.css({ height: 'auto', width: '100%' }),
        T.isWordSearch || y.FirstTime(),
        (function (e) {
          let i = null,
            n = null,
            o = 'crossword',
            r = A['show-alphabet'];
          if (
            ((k = t('<div/>')
              .css({
                position: 'relative',
                gridArea: 'copy',
                'container-type': 'inline-size',
                'container-name': 'copyframe',
              })
              .appendTo(b)),
            (Div = t('<div/>')
              .css({
                fontSize: '11px',
                color: 'black',
                fontFamily: 'sans-serif',
                fontWeight: 'normal',
                backgroundColor: u,
                '-webkit-text-size-adjust': '100%',
                display: x % 43 != 1 ? '' : 'none',
                cursor: 'default',
                textAlign: 'right',
              })
              .attr('aria-hidden', 'true')
              .html(O[0])
              .appendTo(k)
              .css({ width: e })),
            x % 43 != 1 &&
              1 != w &&
              Div.find('span')
                .css({ color: 'black', textDecoration: 'none', cursor: 'pointer' })
                .on('mouseover', function () {
                  i || t(this).css({ color: 'blue', textDecoration: 'underline' });
                })
                .on('mouseout', function () {
                  t(this).css({ color: 'black', textDecoration: 'none' });
                })
                .on('click', function () {
                  if (i) return !1;
                  window.open('https://www.' + o + '-' + R);
                })
                .on('touchend', function () {
                  if (r) return (clearTimeout(i), !1);
                })
                .on('touchstart', function () {
                  if (r)
                    return (
                      (i = window.setTimeout(function () {
                        window.open('https://www.' + o + '-' + R);
                      }, 1e3)),
                      !1
                    );
                })
                .end(),
            '' != P)
          ) {
            n = t('<div/>')
              .css({
                position: 'absolute',
                fontSize: '11px',
                color: 'black',
                fontFamily: 'sans-serif',
                fontWeight: 'normal',
                backgroundColor: u,
                cursor: 'default',
                display: 'block',
                top: 0,
              })
              .addClass('PuzzleCopyright')
              .html(O[0])
              .prependTo(k);
            let i = n.width();
            (n.html(P),
              i + n.width() > e &&
                (m.append(
                  '@container copyframe (max-width: ' +
                    (i + n.width() + 8 + (T.TimerDiv ? T.TimerDiv.width() : 0)) +
                    'px){.PuzzleCopyright{position:relative !important;display:block}}'
                ),
                Div.css({ width: '100%' })));
          }
        })(U),
        T.RunTimer());
      let Z = T.TimerObject;
      (Z.Enabled &&
        (Z.Actions
          ? T.TimerDiv.appendTo(M)
          : T.TimerDiv.css({ float: 'right', marginRight: '4px', marginLeft: '4px' }).prependTo(k),
        0 == Z.OnLoad && (T.TimerDiv.stopTime(), (Z.Stop = !0))),
        y.ProcessHintLetter(),
        (a.get(0).CrossWord = T));
    }));
})(jQuery);
