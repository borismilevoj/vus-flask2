(!(function () {
  try {
    var e =
        'undefined' != typeof window
          ? window
          : 'undefined' != typeof global
            ? global
            : 'undefined' != typeof self
              ? self
              : {},
      t = new e.Error().stack;
    t &&
      ((e._sentryDebugIds = e._sentryDebugIds || {}),
      (e._sentryDebugIds[t] = '7f5f5e20-8923-4cd8-b9b7-69b6ca152325'),
      (e._sentryDebugIdIdentifier = 'sentry-dbid-7f5f5e20-8923-4cd8-b9b7-69b6ca152325'));
  } catch (e) {}
})(),
  (self.webpackChunk_N_E = self.webpackChunk_N_E || []).push([
    [1053, 7703, 8851],
    {
      35152: function (e, t, r) {
        'use strict';
        (r.d(t, {
          IB: function () {
            return s;
          },
          YS: function () {
            return o;
          },
          eC: function () {
            return n;
          },
        }),
          r(26953));
        var a = r(22319),
          n = '_l5tl1g1 $flex lg:$grid $gap-15 sm:$gap-20 lg:$gap-30',
          s = '$grid-rows-3',
          o = (0, a.c)({
            defaultClassName: '_l5tl1g6 _l5tl1g2',
            variantClassNames: {
              active: { false: '_l5tl1g3', true: '_l5tl1g4' },
              hasLargeHeight: { true: '_l5tl1g5' },
            },
            defaultVariants: { active: !1, hasLargeHeight: !1 },
            compoundVariants: [],
          });
      },
      19701: function (e, t, r) {
        'use strict';
        (r.d(t, {
          M0: function () {
            return s;
          },
          XJ: function () {
            return o;
          },
          be: function () {
            return n;
          },
          hA: function () {
            return l;
          },
          z$: function () {
            return i;
          },
        }),
          r(48388),
          r(44765));
        var a = r(22319),
          n = '$text-center',
          s = (0, a.c)({
            defaultClassName:
              '_1wlpjjh1 $mb-10 $font-semibold $sprinkles-text-2xl lg:$sprinkles-text-3xl',
            variantClassNames: {
              center: { true: '$text-center' },
              color: {
                grayOxford: 'text-surface-foreground-0',
                grayEbony: 'text-surface-foreground-0',
              },
            },
            defaultVariants: { color: 'grayOxford', center: !1 },
            compoundVariants: [],
          }),
          o = '_1wc8gem0 $w-full $mx-auto $px-[20px] $max-w-[1400px] $p-20 xl:$p-40',
          l = '$sprinkles-text-xl lg:$sprinkles-text-2xl $font-semibold $text-surface-foreground-0',
          i = (0, a.c)({
            defaultClassName: '_1wlpjjh5 $sprinkles-text-base lg:$sprinkles-text-lg mb-8',
            variantClassNames: {
              center: { true: '$text-center' },
              color: {
                grayHoki: 'text-surface-foreground-1',
                grayOxford: 'text-surface-foreground-1',
              },
            },
            defaultVariants: { color: 'grayHoki', center: !1 },
            compoundVariants: [],
          });
      },
      47978: function (e, t, r) {
        'use strict';
        r.d(t, {
          i: function () {
            return g;
          },
        });
        var a = r(97458),
          n = r(770),
          s = r(24985),
          o = r(21623),
          l = r(51363),
          i = r(91776),
          c = r(73782),
          u = r(34705);
        r(22243);
        var d = (0, r(22319).c)({
          defaultClassName:
            '_zv94tv0 $absolute $right-0 $z-2 $bg-grayEbony $py-4 $px-10 $rounded-tl-lg $rounded-bl-lg $flex $justify-center $items-center',
          variantClassNames: { position: { top: '$top-15', bottom: '$bottom-15' } },
          defaultVariants: { position: 'bottom' },
          compoundVariants: [],
        });
        let g = (e) => {
          let { type: t, position: r } = e,
            g = {
              photo: l.Z,
              video: u.Z,
              'ai-image': s.Z,
              vector: c.Z,
              template: i.Z,
              mockup: o.Z,
            };
          return g[t]
            ? (0, a.jsx)('span', {
                className: d({ position: r }),
                children:
                  null !== g[t] &&
                  (0, a.jsx)(n.J, { as: g[t], size: 'base', className: '$text-white' }),
              })
            : null;
        };
      },
      58901: function (e, t, r) {
        'use strict';
        r.d(t, {
          N: function () {
            return g;
          },
        });
        var a = r(97458),
          n = r(57291),
          s = r(41275),
          o = r(3680),
          l = r(59251),
          i = r(10893),
          c = r(52983),
          u = r(64198);
        let d = (e) => {
            let { categoriesByTheme: t, fromElement: r } = e,
              [n, d] = (0, c.useState)(t[0].group),
              { t: g } = (0, i.$G)('vectorsHome');
            return (0, a.jsxs)(o.fC, {
              onValueChange: (e) => d(e),
              value: n,
              className: 'flex w-full flex-col',
              children: [
                (0, a.jsx)(o.aV, {
                  className: 'mb-8 hidden h-8 shrink-0 justify-start gap-3 lg:flex',
                  'aria-label': 'Categories by theme selector tabs',
                  children: t.map((e, t) =>
                    (0, a.jsx)(
                      o.xz,
                      {
                        className:
                          'flex items-center rounded-full border border-outline-border-0 p-4 text-secondary-0 transition-colors data-[state=active]:border-secondary-0 data-[state=active]:bg-secondary-0 data-[state=active]:text-secondary-foreground-0 hover:border-outline-border-1',
                        value: e.group,
                        'data-cy': 'significantLink-'.concat(++t),
                        children: (0, s.h)(g(e.group)),
                      },
                      e.group
                    )
                  ),
                }),
                t.map((e) => {
                  let { group: t, categories: n } = e;
                  return (0, a.jsxs)(
                    o.VY,
                    {
                      value: t,
                      className: 'lg:data-[state=inactive]:hidden',
                      forceMount: !0,
                      children: [
                        (0, a.jsx)('h3', {
                          className: 'mb-4 text-lg font-medium lg:hidden',
                          children: g(t),
                        }),
                        (0, a.jsx)(l.Draggable, {
                          active: !0,
                          fit: !0,
                          children: (0, a.jsx)('div', {
                            className: 'mb-8 flex gap-4 lg:mb-0 lg:grid lg:grid-cols-8 lg:gap-6',
                            children: n.map((e) =>
                              (0, a.jsx)(u.P, { item: e, fromElement: r }, e.title)
                            ),
                          }),
                        }),
                      ],
                    },
                    t
                  );
                }),
              ],
            });
          },
          g = (e) => {
            let { categoriesByTheme: t, children: r, className: s, fromElement: o } = e;
            return (0, a.jsxs)('section', {
              className: (0, n.cx)('w-full', s),
              children: [r, (0, a.jsx)(d, { categoriesByTheme: t, fromElement: o })],
            });
          };
      },
      64198: function (e, t, r) {
        'use strict';
        r.d(t, {
          P: function () {
            return h;
          },
        });
        var a = r(97458),
          n = r(41275),
          s = r(770),
          o = r(34428),
          l = r(53344),
          i = r.n(l),
          c = r(98821),
          u = r.n(c),
          d = r(58058),
          g = r.n(d),
          f = r(35152),
          p = r(34705);
        r(40215);
        let m = () =>
            (0, a.jsx)('span', {
              className:
                '_g9ut710 $w-35 $h-25 $text-white $flex $items-center $justify-center $absolute $top-10 $right-0 $rounded-tl-md $rounded-bl-md $z-2',
              children: (0, a.jsx)(s.J, { as: p.Z }),
            }),
          b = i()(
            () =>
              r
                .e(8851)
                .then(r.bind(r, 28851))
                .then((e) => e.VideoContentComponent),
            { loadableGenerated: { webpack: () => [28851] } }
          ),
          x = (e) => {
            let { previews: t } = e;
            return t.length > 1
              ? (0, a.jsxs)(a.Fragment, {
                  children: [
                    (0, a.jsx)(m, {}),
                    (0, a.jsx)(b, {
                      classNames:
                        'opacity-100 w-full h-full object-cover rounded-xl transition-transform hover:scale-[1.03]',
                      poster: t[0].url,
                      videoSrc: t[1].url,
                      isInViewport: !0,
                    }),
                  ],
                })
              : (0, a.jsx)(u(), {
                  alt: '',
                  src: t[0].url,
                  width: 0,
                  height: 0,
                  sizes: '100vw',
                  className:
                    'size-full rounded-xl object-cover transition-transform hover:scale-[1.03]',
                  draggable: !1,
                  loading: 'lazy',
                  onContextMenu: (e) => e.preventDefault(),
                });
          },
          h = (e) => {
            let { item: t, isLargeItem: r = !1, fromElement: l, hasLargeHeight: i = !1 } = e;
            return (0, a.jsxs)(g(), {
              href: ''.concat(t.url, '#from_element=').concat(l),
              className: 'group '.concat(f.YS({ active: r, hasLargeHeight: i })),
              draggable: !1,
              children: [
                (0, a.jsx)(x, { previews: t.previews }),
                (0, a.jsx)('div', {
                  className:
                    'pointer-events-none absolute left-0 top-0 size-full bg-gradient-to-b from-transparent from-40% to-black/50',
                }),
                (0, a.jsx)('p', {
                  className:
                    'pointer-events-none absolute bottom-0 left-0 flex w-full flex-col justify-end p-4 text-base font-medium text-white',
                  children: (0, n.h)(t.title),
                }),
                (0, a.jsx)(s.J, {
                  className: 'absolute bottom-5 right-5 hidden text-white group-hover:block',
                  as: o.Z,
                  size: 'lg',
                }),
                (0, a.jsx)('div', {
                  className:
                    'pointer-events-none absolute left-0 top-0 flex size-full flex-col justify-end bg-gradient-to-b from-transparent to-black/40 p-20 text-sm font-semibold text-white opacity-0 transition-opacity group-hover:opacity-100',
                }),
              ],
            });
          };
      },
      47253: function (e, t, r) {
        'use strict';
        r.d(t, {
          h: function () {
            return u;
          },
        });
        var a = r(97458),
          n = r(16388),
          s = r.n(n);
        let o = Object.freeze({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&apos;',
          }),
          l = RegExp('['.concat(Object.keys(o).join(''), ']'), 'g'),
          i = (e) => o[e],
          c = (e, t) => {
            switch (typeof t) {
              case 'object':
                if (null === t) return;
                return t;
              case 'number':
              case 'boolean':
              case 'bigint':
                return t;
              case 'string':
                return t.replace(l, i);
              default:
                return;
            }
          },
          u = (e) => {
            let { data: t } = e;
            return (0, a.jsx)(s(), {
              children: (0, a.jsx)('script', {
                type: 'application/ld+json',
                dangerouslySetInnerHTML: { __html: JSON.stringify(t, c) },
              }),
            });
          };
      },
      10807: function (e, t, r) {
        'use strict';
        r.d(t, {
          P: function () {
            return m;
          },
        });
        var a = r(97458),
          n = r(87420),
          s = r(52983),
          o = r(98821),
          l = r.n(o),
          i = r(58058),
          c = r.n(i);
        let u = (e, t, r) => ({
            url: ''.concat(e.url[r] || e.url.en, '#from_element=').concat(t),
            title: e.title[r] || e.title.en,
            paragraph: e.paragraph[r] || e.paragraph.en,
            bgImage: 'object' == typeof e.bg_image ? e.bg_image[r] : e.bg_image,
          }),
          d = (e) => {
            let { item: t, fromElement: r, language: a } = e;
            return (0, s.useMemo)(() => u(t, r, a), [t, a, r]);
          },
          g = (e) => {
            let { item: t, fromElement: r, language: n } = e,
              {
                url: s,
                title: o,
                paragraph: i,
                bgImage: u,
              } = d({ item: t, fromElement: r, language: n });
            return (0, a.jsxs)(c(), {
              href: s,
              className: 'group',
              children: [
                (0, a.jsx)('div', {
                  className: 'relative mb-5 aspect-tv overflow-hidden rounded-lg',
                  children: (0, a.jsx)(l(), {
                    src: u,
                    alt: o,
                    fill: !0,
                    className:
                      'object-cover transition-transform duration-300 ease-in-out group-hover:scale-105',
                  }),
                }),
                (0, a.jsxs)('div', {
                  children: [
                    (0, a.jsx)('h3', {
                      className: 'mb-3 text-lg font-semibold text-surface-foreground-0 lg:text-xl',
                      children: o,
                    }),
                    (0, a.jsx)('p', {
                      className:
                        'whitespace-pre-line text-sm text-surface-foreground-4 lg:text-base',
                      children: i,
                    }),
                  ],
                }),
              ],
            });
          },
          f = (e) => {
            let { items: t, fromElement: r = 'articles_block', language: n } = e;
            return (0, a.jsx)(a.Fragment, {
              children: t.map((e) =>
                (0, a.jsx)(
                  s.Fragment,
                  { children: (0, a.jsx)(g, { item: e, fromElement: r, language: n }) },
                  e.id
                )
              ),
            });
          };
        var p = r(19701);
        let m = (e) => {
          let { items: t, title: r, fromElement: s, headingTag: o = 'h2' } = e,
            l = (0, n.ZK)();
          return (0, a.jsxs)('section', {
            className: 'w-full',
            children: [
              (0, a.jsx)('header', { children: (0, a.jsx)(o, { className: p.hA, children: r }) }),
              (0, a.jsx)('div', {
                className: 'grid grid-cols-1 gap-8 py-8 lg:grid-cols-3',
                id: 'blog-articles',
                children: (0, a.jsx)(f, { language: l, items: t, fromElement: s }),
              }),
            ],
          });
        };
      },
      2149: function (e, t, r) {
        'use strict';
        r.d(t, {
          s: function () {
            return i;
          },
        });
        var a = r(97458),
          n = r(59251),
          s = r(33523),
          o = r(78364);
        let l = Array.from({ length: 9 }).map((e, t) =>
            (0, a.jsx)(
              'div',
              {
                className:
                  'relative block h-[264px] w-[380px] cursor-pointer overflow-hidden rounded 2xl-legacy:h-[220px] 2xl-legacy:w-full 2xl-legacy:rounded-none 2xl-legacy:first:col-span-2 2xl-legacy:first:row-span-2 2xl-legacy:first:h-[450px]',
                children: (0, a.jsx)(s.O.Rect, { className: 'h-[inherit] w-full' }),
              },
              'skeleton-'.concat(t)
            )
          ),
          i = (e) => {
            let { isDraggable: t, isLoading: r, type: s, children: i } = e;
            return (0, a.jsx)('div', {
              style: { gridArea: 'trends' },
              children: (0, a.jsx)(n.Draggable, {
                active: t,
                fit: !0,
                children: (0, a.jsx)('div', {
                  className: (0, o.W)(
                    'flex grid-cols-4 gap-3 2xl-legacy:grid 2xl-legacy:overflow-hidden 2xl-legacy:rounded-[4px]',
                    'video' === s && 'grid-rows-3'
                  ),
                  children: r ? l : i,
                }),
              }),
            });
          };
      },
      27703: function (e, t, r) {
        'use strict';
        (r.r(t),
          r.d(t, {
            TrendsItem: function () {
              return h;
            },
          }));
        var a = r(97458),
          n = r(770),
          s = r(25350),
          o = r(34428),
          l = r(98821),
          i = r.n(l),
          c = r(58058),
          u = r.n(c),
          d = r(10893),
          g = r(52983),
          f = r(47978),
          p = r(28851),
          m = r(87420);
        let b = {
            photo: 'photo',
            vector: 'vector',
            'ai-image': 'photo',
            video: 'video',
            template: 'template',
            mockup: 'mockup',
          },
          x = (e) => {
            let { item: t, type: r, language: a, fromElement: n, fromView: s } = e,
              o = (0, m.L3)(),
              { domain: l } = (0, m.Vx)(),
              i = '#'.concat(['from_element='.concat(n), 'from_view='.concat(s)].join('&'));
            if (!t.url) return null;
            let c = 'string' == typeof t.url ? t.url : t.url[a],
              u = c.includes(l)
                ? c
                : ''
                    .concat(o('/'.concat(t.premium ? 'premium' : 'free', '-').concat(b[r])), '/')
                    .concat(c);
            return ''.concat(u).concat(i);
          },
          h = (e) => {
            let { type: t, item: r, language: l, fromElement: c, fromView: m } = e,
              [b, h] = (0, g.useState)(!1),
              { t: v } = (0, d.$G)('common'),
              y = x({ item: r, type: t || 'photo', language: l, fromElement: c, fromView: m });
            return y
              ? (0, a.jsxs)(u(), {
                  href: y,
                  className:
                    ' group relative block h-[264px] w-[380px] cursor-pointer overflow-hidden rounded-xl  2xl-legacy:h-[220px] 2xl-legacy:w-full 2xl-legacy:first:col-start-1 2xl-legacy:first:col-end-3 2xl-legacy:first:row-start-1 2xl-legacy:first:row-end-3 2xl-legacy:first:h-[450px] ',
                  prefetch: !1,
                  onMouseEnter: () => h(!0),
                  onMouseLeave: () => h(!1),
                  'data-cy': 'videos-category',
                  children: [
                    r.showBadge && (0, a.jsx)(f.i, { type: r.type, position: 'top' }),
                    r.video
                      ? (0, a.jsx)(p.VideoContentComponent, {
                          classNames:
                            'size-full object-cover transition-transform duration-300 hover:scale-[1.03] opacity-100',
                          poster: r.poster,
                          videoSrc: r.video,
                          isInViewport: !0,
                        })
                      : (0, a.jsx)(i(), {
                          alt: '',
                          src: r.poster,
                          width: 380,
                          height: 264,
                          className:
                            'size-full object-cover transition-transform duration-300 hover:scale-[1.03]',
                          fetchPriority: 'high',
                          loading: 'lazy',
                          onContextMenu: (e) => e.preventDefault(),
                        }),
                    (0, a.jsx)('div', {
                      className:
                        'pointer-events-none absolute left-0 top-0 flex size-full flex-col justify-end bg-gradient-to-b from-transparent to-black/40 p-5 text-sm font-semibold text-white transition-opacity '.concat(
                          b ? 'opacity-100' : 'opacity-0'
                        ),
                      children: (0, a.jsxs)(s.z, {
                        variant: 'default',
                        shape: 'rounded',
                        className: 'absolute bottom-5 left-5',
                        children: [v('go'), (0, a.jsx)(n.J, { as: o.Z, size: 'lg' })],
                      }),
                    }),
                  ],
                })
              : null;
          };
      },
      28851: function (e, t, r) {
        'use strict';
        (r.r(t),
          r.d(t, {
            VideoContentComponent: function () {
              return d;
            },
          }));
        var a = r(97458),
          n = r(23113),
          s = r(62897),
          o = r(57291),
          l = r(78364),
          i = r(52983),
          c = r(3223),
          u = r(65229);
        let d = (e) => {
            let {
                duration: t,
                videoSrc: r,
                poster: d,
                isInViewport: f,
                classNames: p = '',
                pauseAndPlay: m = !1,
                id: b = 0,
                premium: x = !1,
                position: h = 0,
                enableGaTracker: v = !1,
                checkHover: y = !1,
                isHovered: j = !1,
                orientation: w,
              } = e,
              N = (0, n.a)('lg'),
              $ = (0, i.useRef)(null),
              k = (0, i.useRef)(null),
              _ = (0, i.useRef)(),
              C = (0, i.useRef)(!1),
              z = (0, i.useRef)(!1),
              V = (0, i.useCallback)(() => {
                let e = k.current;
                e &&
                  (_.current = setTimeout(() => {
                    var t, r, a;
                    ((e.src = e.dataset.src),
                      m
                        ? (C.current ||
                            (null === (r = $.current) || void 0 === r || r.load(),
                            (C.current = !0)),
                          null === (t = $.current) || void 0 === t || t.play())
                        : null === (a = $.current) || void 0 === a || a.load());
                  }, 150));
              }, [m]),
              M = (0, i.useCallback)(() => {
                clearTimeout(_.current);
                let e = k.current;
                if (e) {
                  var t, r;
                  m
                    ? null === (t = $.current) || void 0 === t || t.pause()
                    : (e.removeAttribute('src'),
                      null === (r = $.current) || void 0 === r || r.load());
                }
              }, [m]),
              S = (0, c.z)({ id: b, type: 'video', premium: x, position: h }),
              E = (0, i.useCallback)(() => {
                z.current || (S(), (z.current = !0));
              }, [S]);
            return (0, a.jsxs)(a.Fragment, {
              children: [
                (0, a.jsx)('video', {
                  width: 480,
                  height: 270,
                  className: (0, l.W)(p, u.R),
                  ref: $,
                  preload: 'metadata',
                  onMouseOver: V,
                  onMouseOut: M,
                  onLoadStart: () => {
                    v && E();
                  },
                  autoPlay: N,
                  poster: f ? d : void 0,
                  muted: !0,
                  playsInline: !0,
                  loop: !0,
                  'aria-hidden': 'true',
                  children: f && (0, a.jsx)('source', { ref: k, 'data-src': r, type: 'video/mp4' }),
                }),
                f &&
                  (0, a.jsxs)(a.Fragment, {
                    children: [
                      (0, a.jsx)('div', {
                        role: 'presentation',
                        className: g({ checkHover: y, isHovered: j }),
                      }),
                      (0, a.jsx)('header', {
                        className: (0, o.cx)(
                          'pointer-events-none absolute flex w-full max-w-[calc(100%-20px)] items-baseline justify-end gap-1 transition-all',
                          'vertical' !== w ? 'bottom-4 mx-1' : 'bottom-3 mx-2'
                        ),
                        children:
                          !!t &&
                          (0, a.jsx)('div', {
                            className:
                              'rounded-xl bg-overlay-dialog px-2 py-1 text-xs font-semibold text-white',
                            children: (0, s.Z)(null != t ? t : 0),
                          }),
                      }),
                    ],
                  }),
              ],
            });
          },
          g = (0, o.j)(
            'pointer-events-none absolute inset-0 rounded-xl opacity-0 transition-opacity [background:linear-gradient(180deg,rgba(0,0,0,0.1)_0%,rgba(0,0,0,0.4)_100%)]',
            {
              variants: {
                checkHover: { false: '[article:hover_&]:opacity-100', true: '' },
                isHovered: { false: '', true: 'opacity-100' },
              },
            }
          );
      },
      65229: function (e, t, r) {
        'use strict';
        r.d(t, {
          R: function () {
            return a;
          },
        });
        let a =
          'block absolute w-full h-full object-cover object-center $overflow-hidden rounded-xl left-0 top-0 right-0 bottom-0';
      },
      93898: function (e, t, r) {
        'use strict';
        r.d(t, {
          B: function () {
            return a;
          },
        });
        let a = (0, r(52983).createContext)({});
      },
      80144: function (e, t, r) {
        'use strict';
        r.d(t, {
          i: function () {
            return s;
          },
        });
        var a = r(52983),
          n = r(93898);
        let s = () => (0, a.useContext)(n.B);
      },
      3223: function (e, t, r) {
        'use strict';
        r.d(t, {
          z: function () {
            return o;
          },
        });
        var a = r(52983),
          n = r(80144);
        let s = {
            ai: 'regular',
            photo: 'regular',
            vector: 'regular',
            psd: 'regular',
            icon: 'icon',
            template: 'template',
            mockup: 'mockup',
            video: 'video',
            '3d': '3d',
          },
          o = (e) => {
            let { id: t, type: r, premium: o, position: l } = e,
              { vertical: i, addEventTrackerToQueue: c } = (0, n.i)();
            return (0, a.useCallback)(() => {
              var e;
              let a = {
                item_id: t.toString(),
                is_premium_item: o ? '1' : '0',
                position: l.toString(),
                item_supertype: null !== (e = s[r]) && void 0 !== e ? e : r,
                vertical: null != i ? i : r,
              };
              null == c || c(a);
            }, [c, t, l, o, r, i]);
          };
      },
      38171: function (e, t, r) {
        'use strict';
        r.d(t, {
          L: function () {
            return c;
          },
        });
        var a = r(97458),
          n = r(87420),
          s = r(52983),
          o = r(47253);
        let l = {
            photo: '/popular-photos',
            vector: '/vectors',
            psd: '/popular-psd',
            illustration: '/illustrations',
          },
          i = {
            '@type': 'Thing',
            '@id': 'https://www.wikidata.org/wiki/Q1634416',
            name: 'stock photography',
            sameAs: 'https://en.wikipedia.org/wiki/Stock_photography',
          },
          c = (e) => {
            let { url: t, faqs: r, relatedLinks: c, metas: u } = e,
              {
                type: d,
                seo: { title: g, description: f },
                about: p,
              } = u,
              { domain: m, locale: b } = (0, n.Vx)(),
              x = (0, n.$T)(l[d]),
              h = (0, s.useMemo)(() => {
                let e = c
                    .map((e) => {
                      let { url: t } = e;
                      return t;
                    })
                    .slice(0, 10),
                  a = 'photo' === d ? i : p,
                  n = r.map((e) => {
                    let { title: t, content: r } = e;
                    return {
                      '@type': 'Question',
                      name: t,
                      acceptedAnswer: { '@type': 'Answer', text: r.replace(/(<([^>]+)>)|"/g, '') },
                    };
                  });
                return {
                  '@context': 'https://schema.org',
                  '@graph': [
                    {
                      '@type': 'WebPage',
                      url: t,
                      '@id': ''.concat(t, '#webpage'),
                      name: g,
                      description: f,
                      inLanguage: b,
                      relatedLink: ''.concat(m).concat(x),
                      significantLink: e,
                      isPartOf: { '@id': ''.concat(m, '#website') },
                      about: a,
                      hasPart: { '@type': 'FAQPage', '@id': ''.concat(t, '#faq'), mainEntity: n },
                    },
                  ],
                };
              }, [p, f, m, r, b, c, x, g, d, t]);
            return (0, a.jsx)(o.h, { data: h });
          };
      },
      88089: function (e, t, r) {
        'use strict';
        r.d(t, {
          q: function () {
            return s;
          },
        });
        var a = r(97458),
          n = r(39995);
        let s = (e) => {
          let { faqs: t } = e;
          return (0, a.jsxs)('div', {
            className: 'pb-8 pt-12 lg:pb-20 lg:pt-32',
            children: [
              (0, a.jsx)('h2', {
                className: 'typo-heading-xs mb-4 lg:typo-heading-sm lg:mb-8',
                children: 'FAQ',
              }),
              (0, a.jsx)(n.c2, {
                children: t.map((e) => {
                  let { title: t, content: r } = e;
                  return (0, a.jsxs)(
                    n.Qd,
                    {
                      children: [
                        (0, a.jsx)(n.vK, { as: 'h3', children: t }),
                        (0, a.jsx)(n._p, {
                          forceMount: !0,
                          children: (0, a.jsx)('p', {
                            className: '[&_a]:font-semibold [&_a]:text-piki-blue-500',
                            dangerouslySetInnerHTML: { __html: r },
                          }),
                        }),
                      ],
                    },
                    t
                  );
                }),
              }),
            ],
          });
        };
      },
      2132: function (e, t, r) {
        'use strict';
        r.d(t, {
          v: function () {
            return m;
          },
        });
        var a = r(97458),
          n = r(770),
          s = r(57291),
          o = r(98821),
          l = r.n(o),
          i = r(58058),
          c = r.n(i),
          u = r(52983),
          d = r(12976);
        let g = (0, s.j)(
            'relative mb-8 h-[200px] overflow-hidden rounded font-semibold sm:h-[320px] lg:mb-0',
            { variants: { odd: { true: null, false: 'order-none lg:order-1' } } }
          ),
          f = (0, s.j)(null, {
            variants: { odd: { true: 'pl-0 lg:pl-20', false: 'pr-0 lg:pr-20' } },
          }),
          p = (e) => {
            let { resource: t } = e,
              [s, o] = (0, u.useState)(!1),
              [i, g] = (0, u.useState)(null);
            if (
              ((0, u.useEffect)(() => {
                s &&
                  !i &&
                  r
                    .e(1968)
                    .then(r.bind(r, 24488))
                    .then((e) => {
                      g(() => e.default);
                    });
              }, [s, i]),
              !t)
            )
              return (0, a.jsx)(l(), {
                alt: 'empty image',
                src: d.r,
                className: 'object-cover transition-transform',
                fill: !0,
              });
            let { name: f, url: p, poster: m, author: b } = t;
            return (0, a.jsxs)(c(), {
              href: p,
              className: 'size-full [&_img]:hover:scale-105',
              prefetch: !1,
              onMouseEnter: () => o(!0),
              onMouseLeave: () => o(!1),
              children: [
                (0, a.jsx)(l(), {
                  alt: f,
                  src: m,
                  className: 'object-cover transition-transform',
                  fill: !0,
                }),
                (0, a.jsxs)('div', {
                  className:
                    'absolute left-0 top-0 flex size-full flex-col justify-end bg-gradient-to-t from-black/40 to-transparent p-5 text-white opacity-0 transition-opacity hover:opacity-100',
                  children: [
                    s && i && (0, a.jsx)(n.J, { className: 'absolute right-5 top-5', as: i }),
                    (0, a.jsx)('p', { children: b }),
                  ],
                }),
              ],
            });
          },
          m = (e) => {
            let { articles: t } = e;
            return (0, a.jsx)('div', {
              className: 'grid gap-12 lg:gap-32',
              children: t.map((e, t) => {
                let { title: r, content: n, resource: s } = e,
                  o = t % 2 == 1;
                return (0, a.jsxs)(
                  'div',
                  {
                    className: 'grid grid-cols-1 items-center justify-center lg:grid-cols-2',
                    children: [
                      (0, a.jsx)('div', {
                        className: g({ odd: o }),
                        children: (0, a.jsx)(p, { resource: s }),
                      }),
                      (0, a.jsxs)('div', {
                        className: f({ odd: o }),
                        children: [
                          (0, a.jsx)('h2', { className: 'mb-6 font-medium', children: r }),
                          (0, a.jsx)('p', {
                            className: 'text-base text-surface-foreground-3',
                            children: n,
                          }),
                        ],
                      }),
                    ],
                  },
                  r
                );
              }),
            });
          };
      },
      39995: function (e, t, r) {
        'use strict';
        r.d(t, {
          Qd: function () {
            return a.Q;
          },
          _p: function () {
            return n._;
          },
          c2: function () {
            return o.c;
          },
          vK: function () {
            return s.v;
          },
        });
        var a = r(87985),
          n = r(72452),
          s = r(24604),
          o = r(91933);
      },
      25350: function (e, t, r) {
        'use strict';
        r.d(t, {
          z: function () {
            return l;
          },
        });
        var a = r(97458),
          n = r(97374),
          s = r(40197);
        let o = (0, r(57291).j)(
          [
            'flex items-center justify-center gap-2 rounded font-semibold transition duration-150 ease-in-out',
            'disabled:cursor-not-allowed disabled:opacity-50',
            'disabled:aria-pressed:cursor-default disabled:aria-pressed:opacity-100',
            'focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-surface-border-10',
            'active:outline-none',
            'text-nowrap',
          ],
          {
            variants: {
              size: { sm: 'text-xs px-4 h-8', md: 'text-sm px-4 h-10', lg: 'text-base px-6 h-12' },
              shape: { rectangle: 'rounded', rounded: 'rounded-full' },
              variant: {
                primary: [
                  'bg-primary-0 text-primary-foreground-0 aria-pressed:bg-primary-2 hover:bg-primary-1 active:bg-primary-2 disabled:bg-primary-0 disabled:aria-pressed:bg-primary-0',
                ],
                secondary: [
                  'bg-secondary-0 text-secondary-foreground-0 aria-pressed:bg-secondary-2 hover:bg-secondary-1 active:bg-secondary-2 disabled:bg-secondary-0 disabled:aria-pressed:bg-secondary-0',
                ],
                tertiary: [
                  'bg-default-0 text-default-foreground-0 aria-pressed:bg-default-2 hover:bg-default-1 active:bg-default-2 disabled:bg-default-0 disabled:aria-pressed:bg-default-2',
                ],
                outline: [
                  'border border-outline-border-0 bg-outline-0 text-outline-foreground-0 aria-pressed:bg-outline-1 hover:border-outline-border-1 active:border-outline-border-2 active:bg-outline-1 disabled:border-outline-border-0 disabled:aria-pressed:border-outline-border-0',
                ],
                default: [
                  'bg-surface-0 text-default-foreground-0 aria-pressed:bg-surface-2 hover:bg-surface-1 active:bg-surface-3 disabled:bg-surface-0 disabled:aria-pressed:bg-surface-0',
                ],
                ghost: [
                  'bg-ghost-0 text-ghost-foreground-0 aria-pressed:bg-ghost-2 hover:bg-ghost-1 active:bg-ghost-2 disabled:bg-ghost-0 disabled:aria-pressed:bg-ghost-0',
                ],
                premium: [
                  'bg-premium-0 text-premium-foreground-0 aria-pressed:bg-premium-2 hover:bg-premium-1 active:bg-premium-2 disabled:bg-premium-0 disabled:aria-pressed:bg-premium-0',
                ],
                destructive: [
                  'bg-destructive-0 text-destructive-foreground-0 aria-pressed:bg-destructive-1 hover:bg-destructive-1 active:bg-destructive-1 disabled:bg-destructive-0 disabled:aria-pressed:bg-destructive-0',
                ],
              },
            },
            defaultVariants: { variant: 'primary', size: 'md', shape: 'rectangle' },
          }
        );
        function l(e) {
          let { className: t, variant: r, size: l, shape: i, asChild: c = !1, ...u } = e,
            d = c ? n.g7 : 'button';
          return (0, a.jsx)(d, {
            className: (0, s.m6)(o({ variant: r, size: l, shape: i }), t),
            ...u,
          });
        }
      },
      41275: function (e, t, r) {
        'use strict';
        r.d(t, {
          h: function () {
            return a;
          },
        });
        let a = (e) => (e ? ''.concat(e[0].toUpperCase()).concat(e.slice(1)) : e);
      },
      62897: function (e, t, r) {
        'use strict';
        r.d(t, {
          Z: function () {
            return s;
          },
          w: function () {
            return o;
          },
        });
        let a = (e) => (e < 10 ? '0'.concat(e) : e),
          n = (e) => {
            let t = Math.floor(e / 60);
            return { minutes: t, seconds: e - 60 * t };
          },
          s = function (e) {
            let t = !(arguments.length > 1) || void 0 === arguments[1] || arguments[1],
              { minutes: r, seconds: s } = n(e);
            return t ? ''.concat(a(r), ':').concat(a(s)) : ''.concat(r, ':').concat(a(s));
          },
          o = (e) => {
            let { minutes: t, seconds: r } = n(e),
              a = 'PT';
            return (t > 0 && (a += ''.concat(t, 'M')), (a += ''.concat(r, 'S')));
          };
      },
      22243: function () {},
    },
  ]));
