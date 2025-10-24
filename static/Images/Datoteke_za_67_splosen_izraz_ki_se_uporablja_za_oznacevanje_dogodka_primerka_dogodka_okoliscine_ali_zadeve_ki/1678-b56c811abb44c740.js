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
      (e._sentryDebugIds[t] = 'e2ecf162-146a-4073-9501-6b83c937b76c'),
      (e._sentryDebugIdIdentifier = 'sentry-dbid-e2ecf162-146a-4073-9501-6b83c937b76c'));
  } catch (e) {}
})(),
  (self.webpackChunk_N_E = self.webpackChunk_N_E || []).push([
    [1678],
    {
      82164: function (e, t, a) {
        'use strict';
        a.d(t, {
          S: function () {
            return u;
          },
        });
        var r = a(97458),
          s = a(23113),
          n = a(81157),
          l = a(770),
          o = a(74447),
          i = a(10893),
          c = a(52983);
        let u = (e) => {
          let { path: t, terms: a, fromElement: u, showLabel: d = !0, isAQuerySearch: f = !1 } = e,
            { t: b } = (0, i.$G)('common'),
            x = (0, s.a)('smMax') ? 2 : a.length,
            g = a.slice(0, x),
            p = (0, c.useId)(),
            v = (e) => {
              if (f) {
                let a = e.fileType ? '&file_type='.concat(e.fileType) : '',
                  r = !e.fileType && e.slug ? '&query='.concat(e.slug) : '';
                return ''.concat(t).concat(a).concat(r, '#from_element=').concat(u);
              }
              return ''.concat(t, '/').concat(e.slug, '#from_element=').concat(u);
            };
          return (0, r.jsxs)('ul', {
            className: 'mx-auto flex items-center justify-center gap-3',
            children: [
              d &&
                (0, r.jsxs)('li', {
                  className: 'hidden whitespace-nowrap text-xs font-semibold md:block',
                  children: [b('popularSearches'), ':'],
                }),
              g.map((e, t) => {
                let a = v(e);
                return (0, r.jsx)(
                  'li',
                  {
                    children: (0, r.jsxs)(n.gg, {
                      id: 'popular-searches-'.concat(p, '-').concat(t),
                      as: 'a',
                      color: 'transparent',
                      radius: 'sm',
                      size: 'xs',
                      href: a,
                      className:
                        'rounded-full border border-surface-border-1 hover:border-surface-border-2',
                      children: [
                        (0, r.jsx)(l.J, { as: o.Z, size: 'xs', className: '$mr-5' }),
                        e.title.toLowerCase(),
                      ],
                    }),
                  },
                  e.slug
                );
              }),
            ],
          });
        };
      },
      61130: function (e, t, a) {
        'use strict';
        a.d(t, {
          O: function () {
            return n;
          },
        });
        var r = a(97458),
          s = a(40197);
        let n = (e) => {
          let { children: t, isUserAuthenticated: a, className: n } = e;
          return (0, r.jsx)('div', {
            className: (0, s.m6)(
              'relative mx-auto w-full flex flex-col items-start max-w-[1440px] overflow-hidden gap-8 sm:gap-16 2xl:gap-24',
              a ? 'mt-0 lg:mt-10' : 'mt-20',
              'px-5 xl:px-8',
              n
            ),
            children: t,
          });
        };
      },
      41571: function (e, t, a) {
        'use strict';
        a.d(t, {
          p: function () {
            return r.pD;
          },
          r: function () {
            return s;
          },
        });
        var r = a(52215);
        let s = ''.concat(r.pD, '/collections/images/no-resources.svg');
      },
      12976: function (e, t, a) {
        'use strict';
        a.d(t, {
          p: function () {
            return r.p;
          },
          r: function () {
            return r.r;
          },
        });
        var r = a(41571);
      },
      51565: function (e, t, a) {
        'use strict';
        a.d(t, {
          t: function () {
            return x;
          },
        });
        var r = a(97458),
          s = a(7616),
          n = a(52983),
          l = a(40811),
          o = a(99208),
          i = a(46730),
          c = a(8517);
        let u = function () {
          let e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : [],
            t = (0, c.o)(e),
            a = (0, n.useRef)(t);
          return (0, n.useMemo)(() => ((0, i.A1)(a.current, t) || (a.current = t), a.current), [t]);
        };
        var d = a(31861),
          f = a(5704);
        let b = (0, n.createContext)(void 0),
          x = (e) => {
            let { children: t, filters: a } = e,
              i = u(a),
              c = (0, s.b9)(d.GD),
              x = (0, s.b9)(f.lh),
              g = (0, s.b9)(d.r9),
              p = (0, s.b9)(d.tj),
              v = (0, s.b9)(d.LB),
              m = (0, s.b9)(d.a3),
              h = (0, s.b9)(d.Kn),
              w = (0, n.useCallback)(() => {
                i &&
                  (x(i),
                  c(o.w.lastFilterValue('term', i) || l.O.term.defaultValue),
                  g(!1),
                  p(o.w.lastFilterValue('type', i)),
                  v(o.w.lastFilterValue('format', i) || l.O.format.defaultValue),
                  m(o.w.lastFilterValue('license', i)),
                  h(o.w.lastFilterValue('aiGenerated', i)));
              }, [i, c, x, g, p, v, m, h]);
            (0, n.useEffect)(() => {
              w();
            }, [w]);
            let $ = (0, n.useMemo)(() => ({ values: i, reset: w }), [i, w]);
            return (0, r.jsx)(b.Provider, { value: $, children: t });
          };
      },
      34035: function (e, t, a) {
        'use strict';
        a.d(t, {
          p: function () {
            return r;
          },
        });
        let r = (0, a(52983).createContext)(void 0);
      },
      87985: function (e, t, a) {
        'use strict';
        a.d(t, {
          Q: function () {
            return l;
          },
        });
        var r = a(97458),
          s = a(52389),
          n = a(78364);
        let l = (e) => {
          let { children: t, className: a, ...l } = e;
          return (0, r.jsx)(s.fC, {
            asChild: !0,
            ...l,
            children: (0, r.jsx)('li', {
              className: (0, n.W)('flex w-full flex-col py-3', a),
              children: t,
            }),
          });
        };
      },
      72452: function (e, t, a) {
        'use strict';
        a.d(t, {
          _: function () {
            return c;
          },
        });
        var r = a(97458),
          s = a(52389),
          n = a(18503),
          l = a(75373),
          o = a(48028);
        let i = (e) =>
            0 === e
              ? {}
              : 'number' == typeof e
                ? { '--preview-height': ''.concat(e, 'px') }
                : { '--preview-height': e },
          c = (e) => {
            let { className: t, forceMount: a, previewHeight: c = 0, style: u, ...d } = e,
              { forceItemsMount: f, variant: b } = (0, o.K)();
            return (0, r.jsx)(s.VY, {
              ...d,
              className: (0, n.m)(
                (0, l.i9)({ variant: 'underline' === b ? 'base' : b }),
                0 === c
                  ? 'data-[state=closed]:hidden'
                  : 'data-[state=closed]:max-h-[var(--preview-height)]',
                t
              ),
              style: { ...i(c), ...u },
              forceMount: null != a ? a : f,
            });
          };
      },
      24604: function (e, t, a) {
        'use strict';
        a.d(t, {
          v: function () {
            return f;
          },
        });
        var r = a(97458),
          s = a(52389),
          n = a(53100),
          l = a(14417),
          o = a(18503),
          i = a(52983),
          c = a(770),
          u = a(75373),
          d = a(48028);
        let f = (e) => {
          let {
              as: t,
              children: a,
              className: f,
              wrapperClassName: b,
              OpenComponent: x = (0, r.jsx)(c.J, { as: n.Z, size: 'lg' }),
              CloseComponent: g = (0, r.jsx)(c.J, { as: l.Z, size: 'lg' }),
              ...p
            } = e,
            { variant: v } = (0, d.K)(),
            m = 'underline' === v,
            h = (0, i.cloneElement)(g, {
              className: (0, u.Wf)({ visibleOn: 'closed', underline: m }),
            }),
            w = (0, i.cloneElement)(x, {
              className: (0, u.Wf)({ visibleOn: 'open', underline: m }),
            });
          return (0, r.jsx)(null != t ? t : 'h4', {
            className: b,
            children: (0, r.jsxs)(s.xz, {
              className: (0, o.m)((0, u.hk)({ variant: v }), f, 'group/trigger'),
              ...p,
              children: [(0, r.jsx)('span', { className: 'flex-1', children: a }), h, w],
            }),
          });
        };
      },
      91933: function (e, t, a) {
        'use strict';
        a.d(t, {
          c: function () {
            return l;
          },
        });
        var r = a(97458),
          s = a(52983),
          n = a(34035);
        let l = (e) => {
          let { variant: t = 'base', forceItemsMount: a, ...l } = e,
            o = (0, s.useMemo)(() => ({ forceItemsMount: a, variant: t }), [a, t]);
          return (0, r.jsx)(n.p.Provider, { value: o, children: (0, r.jsx)('ul', { ...l }) });
        };
      },
      75373: function (e, t, a) {
        'use strict';
        a.d(t, {
          Wf: function () {
            return n;
          },
          hk: function () {
            return s;
          },
          i9: function () {
            return l;
          },
        });
        var r = a(57291);
        let s = (0, r.j)(
            'leading-relaxed flex w-full items-center justify-between gap-10 text-left',
            {
              variants: {
                variant: {
                  base: 'py-4 text-lg text-surface-foreground-0 data-[state=open]:text-surface-accent-0',
                  solid:
                    'leading-relaxed rounded-lg border border-surface-1 bg-surface-1 px-8 py-5 text-xl text-primary-0',
                  outlined:
                    'dark:data-[state=open]:$border-b-0 leading-relaxed rounded-lg border border-surface-3 px-8 py-5 text-lg text-surface-foreground-2 data-[state=open]:text-surface-accent-0 dark:data-[state=open]:text-surface-accent-0',
                  underline:
                    'border-b border-surface-3 py-4 text-lg text-surface-foreground-2 data-[state=open]:border-b-0 data-[state=open]:text-surface-foreground-2 md:text-xl dark:data-[state=open]:pb-4',
                },
              },
              defaultVariants: { variant: 'base' },
            }
          ),
          n = (0, r.j)('hidden text-surface-foreground-0 data-[state=open]:text-surface-accent-0', {
            variants: {
              visibleOn: {
                open: 'group-data-[state=open]/trigger:inline-block',
                closed: 'group-data-[state=closed]/trigger:inline-block',
              },
              underline: { true: 'group-data-[state=open]/trigger:text-inherit', false: '' },
            },
            defaultVariants: { underline: !1 },
          }),
          l = (0, r.j)('overflow-hidden transition-all duration-300 ease-in-out', {
            variants: {
              variant: {
                base: 'dark:data-[state=closed]:after:from-gray-900 pr-8 text-base text-surface-foreground-2 data-[state=closed]:relative data-[state=closed]:max-h-16 data-[state=closed]:after:pointer-events-none data-[state=closed]:after:absolute data-[state=closed]:after:inset-x-0 data-[state=closed]:after:bottom-0 data-[state=closed]:after:h-8 data-[state=closed]:after:bg-gradient-to-t data-[state=closed]:after:from-white data-[state=closed]:after:to-transparent',
                solid:
                  'dark:bg-surface-3/10 dark:border-surface-3/10 dark:data-[state=closed]:after:from-surface-3/10 leading-relaxed rounded-b-lg border-x border-b border-surface-1 bg-surface-1 px-8 pb-4 text-left text-base text-surface-foreground-2 data-[state=closed]:relative data-[state=closed]:max-h-20 data-[state=closed]:after:pointer-events-none data-[state=closed]:after:absolute data-[state=closed]:after:inset-x-8 data-[state=closed]:after:bottom-4 data-[state=closed]:after:h-8 data-[state=closed]:after:bg-gradient-to-t data-[state=closed]:after:from-surface-1 data-[state=closed]:after:to-transparent dark:text-surface-3',
                outlined:
                  'dark:border-surface-3/10 dark:data-[state=closed]:after:from-gray-900 leading-relaxed rounded-b-lg border-x border-b border-surface-3 px-8 pb-4 text-left text-base text-surface-foreground-2 data-[state=closed]:relative data-[state=closed]:max-h-20 data-[state=closed]:after:pointer-events-none data-[state=closed]:after:absolute data-[state=closed]:after:inset-x-8 data-[state=closed]:after:bottom-4 data-[state=closed]:after:h-8 data-[state=closed]:after:bg-gradient-to-t data-[state=closed]:after:from-white data-[state=closed]:after:to-transparent dark:text-surface-3',
              },
            },
          });
      },
      48028: function (e, t, a) {
        'use strict';
        a.d(t, {
          K: function () {
            return n;
          },
        });
        var r = a(52983),
          s = a(34035);
        let n = () => {
          let e = (0, r.useContext)(s.p);
          if (void 0 === e)
            throw Error('useAccordionConfig must be used within an AccordionConfigProvider');
          return e;
        };
      },
      59251: function (e, t, a) {
        'use strict';
        let r;
        (a.r(t),
          a.d(t, {
            AttentionEffect: function () {
              return j;
            },
            Draggable: function () {
              return i;
            },
            DraggableMobile: function () {
              return c;
            },
            DraggableNavigation: function () {
              return k;
            },
            NavigationButton: function () {
              return m;
            },
          }));
        var s = a(97458),
          n = a(52983);
        a(81602);
        var l = (0, a(22319).c)({
          defaultClassName: '_15qpb3h3 _15qpb3h1 $relative $flex $cursor-grab $overflow-x-auto',
          variantClassNames: {
            fit: { false: '_15qpb3h4', true: '_15qpb3h2 $-mx-20 $overflow-y-hidden' },
            overflowScrolling: { true: '_15qpb3h6' },
          },
          defaultVariants: { fit: !1 },
          compoundVariants: [],
        });
        let o = (e) => {
            let { active: t = !1, ref: a } = e,
              [r, s] = (0, n.useState)(t),
              [l, o] = (0, n.useState)(!1),
              [i, c] = (0, n.useState)(!1),
              [u, d] = (0, n.useState)(0),
              [f, b] = (0, n.useState)(0),
              [x, g] = (0, n.useState)(0),
              [p] = (0, n.useState)(5),
              v = (0, n.useCallback)(
                (e) => {
                  let t = a.current;
                  t && (o(!0), g(e.pageX - t.offsetLeft), d(t.scrollLeft));
                },
                [a]
              ),
              m = (0, n.useCallback)(() => {
                o(!1);
              }, []),
              h = (0, n.useCallback)(
                (e) => {
                  let t = a.current;
                  if (t && l) {
                    e.preventDefault();
                    let a = u - (e.pageX - t.offsetLeft - x);
                    Math.abs(t.scrollLeft - a) > p && (c(!0), b(a), (t.scrollLeft = a));
                  }
                },
                [l, a, u, x, p]
              ),
              w = (0, n.useCallback)(
                (e) => {
                  (i && (e.preventDefault(), e.stopPropagation()), c(!1));
                },
                [i]
              );
            return (
              (0, n.useEffect)(() => {
                if ((s(t), r)) {
                  let e = a.current;
                  return (
                    e &&
                      (e.addEventListener('mousedown', v),
                      e.addEventListener('mouseleave', m),
                      e.addEventListener('mouseup', m),
                      e.addEventListener('mousemove', h),
                      e.addEventListener('click', w)),
                    () => {
                      e &&
                        (e.removeEventListener('mousedown', v),
                        e.removeEventListener('mouseleave', m),
                        e.removeEventListener('mouseup', m),
                        e.removeEventListener('mousemove', h),
                        e.removeEventListener('click', w));
                    }
                  );
                }
              }, [t, r, v, m, h, w, a]),
              { isActive: r, position: f }
            );
          },
          i = (e) => {
            let { active: t = !0, children: a, fit: r = !1 } = e,
              i = (0, n.useRef)(null),
              { isActive: c } = o({ active: t, ref: i });
            return (0, s.jsx)('div', {
              ref: i,
              className: c ? l({ fit: r }) : void 0,
              children: a,
            });
          },
          c = (e) => {
            let { active: t = !0, children: a, fit: r = !1 } = e,
              i = (0, n.useRef)(null),
              { isActive: c } = o({ active: t, ref: i });
            return (0, s.jsx)('div', {
              ref: i,
              className: c ? l({ fit: r }) : '_15qpb3h0',
              children: a,
            });
          };
        var u = a(78364),
          d = a(34224),
          f = a(39266),
          b = a(57291),
          x = a(40197),
          g = a(770),
          p = a(13807),
          v = a.n(p);
        let m = (e) => {
            let {
                position: t,
                style: a,
                onClick: r,
                showCallUserAttentionEffect: l,
                className: o,
                dataCy: i,
                arrowAriaLabel: c,
                size: u = 'base',
              } = e,
              [d, f] = (0, n.useState)(!1),
              b = (0, n.useRef)(!1),
              g = (0, n.useCallback)(() => {
                (d || f(!0), null == r || r());
              }, [d, r]);
            return (
              (0, n.useEffect)(() => {
                d ||
                  !1 !== b.current ||
                  setTimeout(() => {
                    (f(!0), (b.current = !0));
                  }, 1e4);
              }, [d]),
              (0, s.jsxs)('button', {
                onClick: g,
                className: (0, x.m6)(h({ position: t, style: a, size: u }), o),
                'data-cy': i,
                'aria-label': c,
                children: [
                  l && !d && (0, s.jsx)(j, { size: u }),
                  (0, s.jsx)(w, { position: t, size: u, style: a }),
                ],
              })
            );
          },
          h = (0, b.j)(
            '$absolute $inset-y-0  $flex $w-35  $cursor-pointer $items-center $justify-center',
            {
              variants: {
                position: { left: '$-left-15', right: '$-right-15' },
                style: {
                  default:
                    '$bg-surface-0 before:$absolute before:$inset-y-0  before:$w-35 before:$from-white before:$to-transparent before:$content-[""] dark:before:from-surface-0',
                  resources: '',
                },
                size: { base: '', xs: '' },
              },
              compoundVariants: [
                {
                  style: 'default',
                  position: 'left',
                  class: 'before:$left-35 before:$bg-gradient-to-r',
                },
                {
                  style: 'default',
                  position: 'right',
                  class: 'before:$right-35 before:$bg-gradient-to-l',
                },
              ],
            }
          ),
          w = (e) => {
            let { position: t, size: a = 'base', style: r = 'default' } = e;
            return (0, s.jsx)('span', {
              className: $({ size: a, style: r }),
              children: (0, s.jsx)(g.J, { as: 'left' === t ? f.Z : d.Z, size: a }),
            });
          },
          $ = (0, b.j)(
            '$z-0 $flex $items-center  $justify-center hover:$text-surface-foreground-2 text-surface-foreground-2',
            {
              variants: {
                size: { base: '$h-35 $w-35', xs: '$h-[24px] $w-[24px]' },
                style: { default: '', resources: '$rounded-full $bg-surface-0 $shadow-xs ' },
              },
            }
          ),
          j = (e) => {
            let { size: t } = e;
            return (0, s.jsxs)(s.Fragment, {
              children: [
                (0, s.jsx)(y, { size: t, className: v().bigAttention }),
                (0, s.jsx)(y, { size: t, className: v().smallAttention }),
              ],
            });
          },
          y = (e) => {
            let { size: t, className: a } = e;
            return (0, s.jsx)('span', {
              className: (0, b.cx)(
                '$absolute $cursor-default $rounded-full $bg-surface-3 $opacity-40 $backdrop-blur-md',
                a,
                'xs' === t ? '$h-25 $w-25' : '$h-35 $w-35'
              ),
            });
          },
          k = (e) => {
            let {
                children: t,
                style: a = 'default',
                overflowScrolling: i = !0,
                className: c,
                width: d,
                nextNavigationButtonEffect: f,
                navigationClassName: b,
                arrowDataCy: x,
                arrowPrevAriaLabel: g,
                arrowNextAriaLabel: p,
                arrowSize: v,
              } = e,
              h = (0, n.useRef)(null),
              w = (0, n.useRef)(null),
              [$, j] = (0, n.useState)(!1),
              [y, k] = (0, n.useState)(!1),
              { position: N } = o({ active: !0, ref: h }),
              C = (0, n.useCallback)(() => {
                let e = null == h ? void 0 : h.current,
                  t = null == w ? void 0 : w.current;
                if (e && t) {
                  let a = e.offsetWidth,
                    r = t.scrollWidth,
                    s = e.scrollLeft >= r - a;
                  (j(e.scrollLeft > 0), k(r > a && !s));
                }
              }, []),
              E = (0, n.useCallback)(
                function () {
                  let e = arguments.length > 0 && void 0 !== arguments[0] && arguments[0],
                    t = null == h ? void 0 : h.current;
                  if (t) {
                    let a = t.offsetWidth * (e ? 1 : -1);
                    (t.scroll({ left: t.scrollLeft + a / 2, behavior: 'smooth' }),
                      clearTimeout(r),
                      (r = setTimeout(C, 500)));
                  }
                },
                [C]
              );
            return (
              (0, n.useEffect)(() => {
                C();
              }, [N, C]),
              (0, n.useEffect)(() => {
                let e = null == w ? void 0 : w.current,
                  t = new ResizeObserver(C);
                return (
                  e && t.observe(e),
                  () => {
                    e && t.unobserve(e);
                  }
                );
              }, [C]),
              (0, s.jsxs)('div', {
                className: (0, u.W)('$group $relative', c),
                children: [
                  (0, s.jsx)('div', {
                    ref: h,
                    className: l({ overflowScrolling: i }),
                    children: (0, s.jsx)('div', {
                      className: 'full' === d ? '$w-full' : '',
                      ref: w,
                      children: t,
                    }),
                  }),
                  $ &&
                    (0, s.jsx)(m, {
                      position: 'left',
                      style: a,
                      onClick: () => E(),
                      className: b,
                      dataCy: ''.concat(x, '-left'),
                      arrowAriaLabel: g,
                      size: v,
                    }),
                  y &&
                    (0, s.jsx)(m, {
                      position: 'right',
                      style: a,
                      showCallUserAttentionEffect: f,
                      onClick: () => E(!0),
                      className: b,
                      dataCy: ''.concat(x, '-right'),
                      arrowAriaLabel: p,
                      size: v,
                    }),
                ],
              })
            );
          };
      },
      53100: function (e, t, a) {
        'use strict';
        var r = a(97458);
        t.Z = (e) =>
          (0, r.jsx)('svg', {
            xmlns: 'http://www.w3.org/2000/svg',
            viewBox: '-49 141 512 512',
            width: 16,
            height: 16,
            'aria-hidden': !0,
            ...e,
            children: (0, r.jsx)('path', {
              d: 'M413 422H1c-13.807 0-25-11.193-25-25s11.193-25 25-25h412c13.807 0 25 11.193 25 25s-11.193 25-25 25',
            }),
          });
      },
      14417: function (e, t, a) {
        'use strict';
        var r = a(97458);
        t.Z = (e) =>
          (0, r.jsx)('svg', {
            xmlns: 'http://www.w3.org/2000/svg',
            viewBox: '-49 141 512 512',
            width: 16,
            height: 16,
            'aria-hidden': !0,
            ...e,
            children: (0, r.jsx)('path', {
              d: 'M413 372H232V191c0-13.807-11.193-25-25-25s-25 11.193-25 25v181H1c-13.807 0-25 11.193-25 25s11.193 25 25 25h181v181c0 13.807 11.193 25 25 25s25-11.193 25-25V422h181c13.807 0 25-11.193 25-25s-11.193-25-25-25',
            }),
          });
      },
      39266: function (e, t, a) {
        'use strict';
        var r = a(97458);
        t.Z = (e) =>
          (0, r.jsx)('svg', {
            xmlns: 'http://www.w3.org/2000/svg',
            viewBox: '-49 141 512 512',
            width: 16,
            height: 16,
            'aria-hidden': !0,
            ...e,
            children: (0, r.jsx)('path', {
              d: 'm151.856 397 163.322-163.322c9.763-9.763 9.763-25.592 0-35.355s-25.592-9.763-35.355 0l-181 181C93.941 384.203 91.5 390.602 91.5 397s2.441 12.796 7.322 17.678l181 181c9.764 9.763 25.592 9.763 35.355 0s9.763-25.592 0-35.355z',
            }),
          });
      },
      13807: function (e) {
        e.exports = {
          bigAttention: 'attentionEffect_bigAttention__sx2Uw',
          smallAttention: 'attentionEffect_smallAttention__DuzZW',
        };
      },
    },
  ]));
