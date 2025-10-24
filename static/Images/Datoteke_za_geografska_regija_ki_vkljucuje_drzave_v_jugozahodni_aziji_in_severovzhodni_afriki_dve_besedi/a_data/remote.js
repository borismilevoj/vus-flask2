(function (g) {
  var window = this;
  ('use strict');
  var aCC = function (Y) {
      if (Y instanceof g.j$) return Y;
      if (typeof Y.YO == 'function') return Y.YO(!1);
      if (g.mg(Y)) {
        var u = 0,
          n = new g.j$();
        n.next = function () {
          for (;;) {
            if (u >= Y.length) return g.i1;
            if (u in Y) return g.Kc(Y[u++]);
            u++;
          }
        };
        return n;
      }
      throw Error('Not implemented');
    },
    $d$ = function (Y, u, n) {
      if (g.mg(Y)) g.Jy(Y, u, n);
      else
        for (Y = aCC(Y); ; ) {
          var U = Y.next();
          if (U.done) break;
          u.call(n, U.value, void 0, Y);
        }
    },
    uE = function (Y) {
      g.Qp(
        Y,
        'zx',
        Math.floor(Math.random() * 2147483648).toString(36) +
          Math.abs(Math.floor(Math.random() * 2147483648) ^ g.iQ()).toString(36)
      );
      return Y;
    },
    n8 = function (Y, u, n) {
      Array.isArray(n) || (n = [String(n)]);
      g.W5u(Y.G, u, n);
    },
    YUC = function (Y, u) {
      var n = [];
      $d$(
        u,
        function (U) {
          try {
            var k = g.BP.prototype.j.call(this, U, !0);
          } catch (m) {
            if (m == 'Storage: Invalid value was encountered') return;
            throw m;
          }
          k === void 0 ? n.push(U) : g.HxG(k) && n.push(U);
        },
        Y
      );
      return n;
    },
    uAR = function (Y, u) {
      YUC(Y, u).forEach(function (n) {
        g.BP.prototype.remove.call(this, n);
      }, Y);
    },
    no$ = function (Y) {
      if (Y.UD) {
        if (Y.UD.locationOverrideToken)
          return { locationOverrideToken: Y.UD.locationOverrideToken };
        if (Y.UD.latitudeE7 != null && Y.UD.longitudeE7 != null)
          return { latitudeE7: Y.UD.latitudeE7, longitudeE7: Y.UD.longitudeE7 };
      }
      return null;
    },
    UIu = function (Y, u) {
      g.jB(Y, u) || Y.push(u);
    },
    kqX = function (Y) {
      var u = 0,
        n;
      for (n in Y) u++;
      return u;
    },
    mI$ = function (Y, u) {
      return g.Qq(Y, u);
    },
    XyB = function (Y) {
      try {
        return g.$e.JSON.parse(Y);
      } catch (u) {}
      Y = String(Y);
      if (
        /^\s*$/.test(Y)
          ? 0
          : /^[\],:{}\s\u2028\u2029]*$/.test(
              Y.replace(/\\["\\\/bfnrtu]/g, '@')
                .replace(
                  /(?:"[^"\\\n\r\u2028\u2029\x00-\x08\x0a-\x1f]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)[\s\u2028\u2029]*(?=:|,|]|}|$)/g,
                  ']'
                )
                .replace(/(?:^|:|,)(?:[\s\u2028\u2029]*\[)+/g, '')
            )
      )
        try {
          return eval('(' + Y + ')');
        } catch (u) {}
      throw Error('Invalid JSON string: ' + Y);
    },
    U1 = function (Y) {
      if (g.$e.JSON)
        try {
          return g.$e.JSON.parse(Y);
        } catch (u) {}
      return XyB(Y);
    },
    PL$ = function () {
      var Y = k2();
      this.K = Y;
      Y.P2('/client_streamz/youtube/living_room/mdx/channel/opened', g.nx('channel_type'));
    },
    SUL = function () {
      var Y = k2();
      this.K = Y;
      Y.P2('/client_streamz/youtube/living_room/mdx/channel/closed', g.nx('channel_type'));
    },
    CLX = function () {
      var Y = k2();
      this.K = Y;
      Y.P2(
        '/client_streamz/youtube/living_room/mdx/channel/message_received',
        g.nx('channel_type')
      );
    },
    fzL = function () {
      var Y = k2();
      this.K = Y;
      Y.P2('/client_streamz/youtube/living_room/mdx/channel/success');
    },
    QoX = function () {
      var Y = k2();
      this.K = Y;
      Y.P2(
        '/client_streamz/youtube/living_room/mdx/channel/error',
        g.nx('channel_type'),
        g.nx('error_type')
      );
    },
    NLR = function () {
      var Y = k2();
      this.K = Y;
      Y.P2('/client_streamz/youtube/living_room/mdx/browser_channel/pending_maps');
    },
    ivJ = function () {
      var Y = k2();
      this.K = Y;
      Y.P2('/client_streamz/youtube/living_room/mdx/browser_channel/undelivered_maps');
    },
    ZvG = function (Y, u, n, U) {
      var k = new g.UQ(null);
      Y && g.k8(k, Y);
      u && g.mJ(k, u);
      n && g.XD(k, n);
      U && (k.j = U);
      return k;
    },
    TLq = function (Y, u) {
      return new g.$8(Y, u);
    },
    mp = function (Y, u) {
      return Object.prototype.hasOwnProperty.call(Y, u);
    },
    rkC = function (Y, u) {
      return Y === u;
    },
    XP = function (Y, u) {
      this.j = {};
      this.K = [];
      this.Qc = this.size = 0;
      var n = arguments.length;
      if (n > 1) {
        if (n % 2) throw Error('Uneven number of arguments');
        for (var U = 0; U < n; U += 2) this.set(arguments[U], arguments[U + 1]);
      } else if (Y)
        if (Y instanceof XP) for (n = Y.Vv(), U = 0; U < n.length; U++) this.set(n[U], Y.get(n[U]));
        else for (U in Y) this.set(U, Y[U]);
    },
    Pz = function (Y) {
      if (Y.size != Y.K.length) {
        for (var u = 0, n = 0; u < Y.K.length; ) {
          var U = Y.K[u];
          mp(Y.j, U) && (Y.K[n++] = U);
          u++;
        }
        Y.K.length = n;
      }
      if (Y.size != Y.K.length) {
        u = {};
        for (U = n = 0; n < Y.K.length; ) {
          var k = Y.K[n];
          mp(u, k) || ((Y.K[U++] = k), (u[k] = 1));
          n++;
        }
        Y.K.length = U;
      }
    },
    SY = function (Y) {
      this.name = this.id = '';
      this.clientName = 'UNKNOWN_INTERFACE';
      this.app = '';
      this.type = 'REMOTE_CONTROL';
      this.ownerObfuscatedGaiaId = this.obfuscatedGaiaId = this.avatar = this.username = '';
      this.capabilities = new Set();
      this.compatibleSenderThemes = new Set();
      this.experiments = new Set();
      this.theme = 'u';
      new XP();
      this.model = this.brand = '';
      this.year = 0;
      this.chipset = this.osVersion = this.os = '';
      this.mdxDialServerType = 'MDX_DIAL_SERVER_TYPE_UNKNOWN';
      Y &&
        ((this.id = Y.id || Y.name),
        (this.name = Y.name),
        (this.clientName = Y.clientName ? Y.clientName.toUpperCase() : 'UNKNOWN_INTERFACE'),
        (this.app = Y.app),
        (this.type = Y.type || 'REMOTE_CONTROL'),
        (this.username = Y.user || ''),
        (this.avatar = Y.userAvatarUri || ''),
        (this.obfuscatedGaiaId = Y.obfuscatedGaiaId || ''),
        (this.ownerObfuscatedGaiaId = Y.ownerObfuscatedGaiaId || ''),
        (this.theme = Y.theme || 'u'),
        MsL(this, Y.capabilities || ''),
        so$(this, Y.compatibleSenderThemes || ''),
        dIQ(this, Y.experiments || ''),
        (this.brand = Y.brand || ''),
        (this.model = Y.model || ''),
        (this.year = Y.year || 0),
        (this.os = Y.os || ''),
        (this.osVersion = Y.osVersion || ''),
        (this.chipset = Y.chipset || ''),
        (this.mdxDialServerType = Y.mdxDialServerType || 'MDX_DIAL_SERVER_TYPE_UNKNOWN'),
        (Y = Y.deviceInfo)) &&
        ((Y = JSON.parse(Y)),
        (this.brand = Y.brand || ''),
        (this.model = Y.model || ''),
        (this.year = Y.year || 0),
        (this.os = Y.os || ''),
        (this.osVersion = Y.osVersion || ''),
        (this.chipset = Y.chipset || ''),
        (this.clientName = Y.clientName ? Y.clientName.toUpperCase() : 'UNKNOWN_INTERFACE'),
        (this.mdxDialServerType = Y.mdxDialServerType || 'MDX_DIAL_SERVER_TYPE_UNKNOWN'));
    },
    MsL = function (Y, u) {
      Y.capabilities.clear();
      g.BV(u.split(','), g.QC(mI$, GqX)).forEach(function (n) {
        Y.capabilities.add(n);
      });
    },
    so$ = function (Y, u) {
      Y.compatibleSenderThemes.clear();
      g.BV(u.split(','), g.QC(mI$, AkX)).forEach(function (n) {
        Y.compatibleSenderThemes.add(n);
      });
    },
    dIQ = function (Y, u) {
      Y.experiments.clear();
      u.split(',').forEach(function (n) {
        Y.experiments.add(n);
      });
    },
    C8 = function (Y) {
      Y = Y || {};
      this.name = Y.name || '';
      this.id = Y.id || Y.screenId || '';
      this.token = Y.token || Y.loungeToken || '';
      this.uuid = Y.uuid || Y.dialId || '';
      this.idType = Y.screenIdType || 'normal';
    },
    f8 = function (Y, u) {
      return !!u && (Y.id == u || Y.uuid == u);
    },
    joy = function (Y) {
      return {
        name: Y.name,
        screenId: Y.id,
        loungeToken: Y.token,
        dialId: Y.uuid,
        screenIdType: Y.idType,
      };
    },
    KRL = function (Y) {
      return new C8(Y);
    },
    goG = function (Y) {
      return Array.isArray(Y) ? g.dA(Y, KRL) : [];
    },
    Qo = function (Y) {
      return Y
        ? '{name:"' +
            Y.name +
            '",id:' +
            Y.id.substr(0, 6) +
            '..,token:' +
            ((Y.token ? '..' + Y.token.slice(-6) : '-') +
              ',uuid:' +
              (Y.uuid ? '..' + Y.uuid.slice(-6) : '-') +
              ',idType:' +
              Y.idType +
              '}')
        : 'null';
    },
    EoX = function (Y) {
      return Array.isArray(Y) ? '[' + g.dA(Y, Qo).join(',') + ']' : 'null';
    },
    HvJ = function () {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (Y) {
        var u = (Math.random() * 16) | 0;
        return (Y == 'x' ? u : (u & 3) | 8).toString(16);
      });
    },
    yk$ = function (Y) {
      return g.dA(Y, function (u) {
        return { key: u.id, name: u.name };
      });
    },
    VsL = function (Y, u) {
      return g.G$(Y, function (n) {
        return n || u ? (!n != !u ? !1 : n.id == u.id) : !0;
      });
    },
    NC = function (Y, u) {
      return g.G$(Y, function (n) {
        return f8(n, u);
      });
    },
    OvC = function () {
      var Y = (0, g.t6)();
      Y && uAR(Y, Y.K.YO(!0));
    },
    iE = function () {
      var Y = g.ck('yt-remote-connected-devices') || [];
      g.VC(Y);
      return Y;
    },
    FRX = function (Y) {
      if (Y.length == 0) return [];
      var u = Y[0].indexOf('#'),
        n = u == -1 ? Y[0] : Y[0].substring(0, u);
      return g.dA(Y, function (U, k) {
        return k == 0 ? U : U.substring(n.length);
      });
    },
    JkL = function (Y) {
      g.oU('yt-remote-connected-devices', Y, 86400);
    },
    Zl = function () {
      if (qUQ) return qUQ;
      var Y = g.ck('yt-remote-device-id');
      Y || ((Y = HvJ()), g.oU('yt-remote-device-id', Y, 31536e3));
      for (var u = iE(), n = 1, U = Y; g.jB(u, U); ) (n++, (U = Y + '#' + n));
      return (qUQ = U);
    },
    azL = function () {
      var Y = iE(),
        u = Zl();
      g.RU() && g.FG(Y, u);
      Y = FRX(Y);
      if (Y.length == 0)
        try {
          g.xo('remote_sid');
        } catch (n) {}
      else
        try {
          g.Ro('remote_sid', Y.join(','), -1);
        } catch (n) {}
    },
    $IX = function () {
      return g.ck('yt-remote-session-browser-channel');
    },
    Y2g = function () {
      return g.ck('yt-remote-local-screens') || [];
    },
    uJ$ = function () {
      g.oU('yt-remote-lounge-token-expiration', !0, 86400);
    },
    nUq = function (Y) {
      Y.length > 5 && (Y = Y.slice(Y.length - 5));
      var u = g.dA(Y2g(), function (U) {
          return U.loungeToken;
        }),
        n = g.dA(Y, function (U) {
          return U.loungeToken;
        });
      g.GZ(n, function (U) {
        return !g.jB(u, U);
      }) && uJ$();
      g.oU('yt-remote-local-screens', Y, 31536e3);
    },
    Tx = function (Y) {
      Y || (g.vk('yt-remote-session-screen-id'), g.vk('yt-remote-session-video-id'));
      azL();
      Y = iE();
      g.pR(Y, Zl());
      JkL(Y);
    },
    UxC = function () {
      if (!r_) {
        var Y = g.xv();
        Y && (r_ = new g.pE(Y));
      }
    },
    kP$ = function () {
      UxC();
      return r_ ? !!r_.get('yt-remote-use-staging-server') : !1;
    },
    MC = function (Y, u) {
      g.Fu[Y] = !0;
      var n = g.VH();
      n && n.publish.apply(n, arguments);
      g.Fu[Y] = !1;
    },
    mxC = function () {},
    k2 = function () {
      if (!s1) {
        s1 = new g.bs(new mxC());
        var Y = g.MI('client_streamz_web_flush_count', -1);
        Y !== -1 && (s1.X = Y);
      }
      return s1;
    },
    Xk$ = function () {
      var Y = window.navigator.userAgent.match(/Chrome\/([0-9]+)/);
      return Y ? parseInt(Y[1], 10) : 0;
    },
    PWJ = function (Y) {
      return (
        !!document.currentScript &&
        (document.currentScript.src.indexOf('?' + Y) != -1 ||
          document.currentScript.src.indexOf('&' + Y) != -1)
      );
    },
    S2$ = function () {
      return typeof window.__onGCastApiAvailable == 'function'
        ? window.__onGCastApiAvailable
        : null;
    },
    d_ = function (Y) {
      Y.length
        ? CWy(Y.shift(), function () {
            d_(Y);
          })
        : fmQ();
    },
    QUu = function (Y) {
      return 'chrome-extension://' + Y + '/cast_sender.js';
    },
    CWy = function (Y, u, n) {
      var U = document.createElement('script');
      U.onerror = u;
      n && (U.onload = n);
      g.Aq(U, g.Aw(Y));
      (document.head || document.documentElement).appendChild(U);
    },
    NTR = function () {
      var Y = Xk$(),
        u = [];
      if (Y > 1) {
        var n = Y - 1;
        u.push('//www.gstatic.com/eureka/clank/' + Y + '/cast_sender.js');
        u.push('//www.gstatic.com/eureka/clank/' + n + '/cast_sender.js');
      }
      return u;
    },
    fmQ = function () {
      var Y = S2$();
      Y && Y(!1, 'No cast extension found');
    },
    ZbG = function () {
      if (ibB) {
        var Y = 2,
          u = S2$(),
          n = function () {
            Y--;
            Y == 0 && u && u(!0);
          };
        window.__onGCastApiAvailable = n;
        CWy('//www.gstatic.com/cast/sdk/libs/sender/1.0/cast_framework.js', fmQ, n);
      }
    },
    TT$ = function () {
      ZbG();
      var Y = NTR();
      Y.push('//www.gstatic.com/eureka/clank/cast_sender.js');
      d_(Y);
    },
    MoX = function () {
      ZbG();
      var Y = NTR();
      Y.push.apply(Y, g.Zu(r6q.map(QUu)));
      Y.push('//www.gstatic.com/eureka/clank/cast_sender.js');
      d_(Y);
    },
    Gx = function (Y, u, n) {
      g.e.call(this);
      this.W = n != null ? (0, g.fR)(Y, n) : Y;
      this.Qu = u;
      this.J = (0, g.fR)(this.uj, this);
      this.K = !1;
      this.j = 0;
      this.X = this.C0 = null;
      this.G = [];
    },
    Ai = function () {},
    sUg = function () {
      g.Vy.call(this, 'p');
    },
    dxX = function () {
      g.Vy.call(this, 'o');
    },
    A6C = function () {
      return (GPX = GPX || new g.is());
    },
    jUB = function (Y) {
      g.Vy.call(this, 'serverreachability', Y);
    },
    jY = function (Y) {
      var u = A6C();
      u.dispatchEvent(new jUB(u, Y));
    },
    KHg = function (Y) {
      g.Vy.call(this, 'statevent', Y);
    },
    K8 = function (Y) {
      var u = A6C();
      u.dispatchEvent(new KHg(u, Y));
    },
    pkG = function (Y, u, n, U) {
      g.Vy.call(this, 'timingevent', Y);
      this.size = u;
      this.rtt = n;
      this.retries = U;
    },
    p8 = function (Y, u) {
      if (typeof Y !== 'function') throw Error('Fn must not be null and must be a function');
      return g.$e.setTimeout(function () {
        Y();
      }, u);
    },
    L8 = function () {},
    ti = function (Y, u, n, U) {
      this.X = Y;
      this.G = u;
      this.CT = n;
      this.lN = U || 1;
      this.Iu = new g.rH(this);
      this.Pz = 45e3;
      this.Fk = null;
      this.W = !1;
      this.N = this.TZ = this.Z = this.JJ = this.jG = this.Uc = this.KG = null;
      this.oV = [];
      this.K = null;
      this.S = 0;
      this.J = this.DW = null;
      this.Ru = -1;
      this.MF = !1;
      this.dg = 0;
      this.zZ = null;
      this.Gw = this.CG = this.nT = this.rg = !1;
      this.j = new LH$();
    },
    LH$ = function () {
      this.j = null;
      this.K = '';
      this.X = !1;
    },
    BTR = function (Y, u, n) {
      Y.JJ = 1;
      Y.Z = uE(u.clone());
      Y.N = n;
      Y.rg = !0;
      tou(Y, null);
    },
    tou = function (Y, u) {
      Y.jG = Date.now();
      Bz(Y);
      Y.TZ = Y.Z.clone();
      n8(Y.TZ, 't', Y.lN);
      Y.S = 0;
      var n = Y.X.JJ;
      Y.j = new LH$();
      Y.K = oUC(Y.X, n ? u : null, !Y.N);
      Y.dg > 0 && (Y.zZ = new g.qs((0, g.fR)(Y.LS, Y, Y.K), Y.dg));
      Y.Iu.listen(Y.K, 'readystatechange', Y.DS);
      u = Y.Fk ? g.rc(Y.Fk) : {};
      Y.N
        ? (Y.DW || (Y.DW = 'POST'),
          (u['Content-Type'] = 'application/x-www-form-urlencoded'),
          Y.K.send(Y.TZ, Y.DW, Y.N, u))
        : ((Y.DW = 'GET'), Y.K.send(Y.TZ, Y.DW, null, u));
      jY(1);
    },
    vUJ = function (Y) {
      if (!c6u(Y)) return g.JH(Y.K);
      var u = g.qE(Y.K);
      if (u === '') return '';
      var n = '',
        U = u.length,
        k = g.O6(Y.K) == 4;
      if (!Y.j.j) {
        if (typeof TextDecoder === 'undefined') return (oO(Y), cz(Y), '');
        Y.j.j = new g.$e.TextDecoder();
      }
      for (var m = 0; m < U; m++)
        ((Y.j.X = !0), (n += Y.j.j.decode(u[m], { stream: !(k && m == U - 1) })));
      u.length = 0;
      Y.j.K += n;
      Y.S = 0;
      return Y.j.K;
    },
    c6u = function (Y) {
      return Y.K ? Y.DW == 'GET' && Y.JJ != 2 && Y.X.sx : !1;
    },
    xxC = function (Y, u) {
      var n = Y.S,
        U = u.indexOf('\n', n);
      if (U == -1) return ReG;
      n = Number(u.substring(n, U));
      if (isNaN(n)) return Dxg;
      U += 1;
      if (U + n > u.length) return ReG;
      u = u.slice(U, U + n);
      Y.S = U + n;
      return u;
    },
    Bz = function (Y) {
      Y.Uc = Date.now() + Y.Pz;
      lmB(Y, Y.Pz);
    },
    lmB = function (Y, u) {
      if (Y.KG != null) throw Error('WatchDog timer not null');
      Y.KG = p8((0, g.fR)(Y.rT, Y), u);
    },
    heL = function (Y) {
      Y.KG && (g.$e.clearTimeout(Y.KG), (Y.KG = null));
    },
    cz = function (Y) {
      Y.X.cW() || Y.MF || wkR(Y.X, Y);
    },
    oO = function (Y) {
      heL(Y);
      g.nc(Y.zZ);
      Y.zZ = null;
      Y.Iu.removeAll();
      if (Y.K) {
        var u = Y.K;
        Y.K = null;
        u.abort();
        u.dispose();
      }
    },
    Hbg = function (Y, u) {
      try {
        var n = Y.X;
        if (n.EE != 0 && (n.K == Y || WHg(n.j, Y)))
          if (!Y.CG && WHg(n.j, Y) && n.EE == 3) {
            try {
              var U = n.tS.K.parse(u);
            } catch (K) {
              U = null;
            }
            if (Array.isArray(U) && U.length == 3) {
              var k = U;
              if (k[0] == 0)
                a: {
                  if (!n.Z) {
                    if (n.K)
                      if (n.K.jG + 3e3 < Y.jG) (vz(n), RO(n));
                      else break a;
                    eeL(n);
                    K8(18);
                  }
                }
              else
                ((n.UD = k[1]),
                  0 < n.UD - n.zZ &&
                    k[2] < 37500 &&
                    n.CG &&
                    n.oV == 0 &&
                    !n.KG &&
                    (n.KG = p8((0, g.fR)(n.y8, n), 6e3)));
              if (bbu(n.j) <= 1 && n.Ub) {
                try {
                  n.Ub();
                } catch (K) {}
                n.Ub = void 0;
              }
            } else Dl(n, 11);
          } else if (((Y.CG || n.K == Y) && vz(n), !g.vq(u)))
            for (k = n.tS.K.parse(u), u = 0; u < k.length; u++) {
              var m = k[u];
              n.zZ = m[0];
              m = m[1];
              if (n.EE == 2)
                if (m[0] == 'c') {
                  n.G = m[1];
                  n.lN = m[2];
                  var X = m[3];
                  X != null && (n.OB = X);
                  var S = m[5];
                  S != null && typeof S === 'number' && S > 0 && (n.dg = 1.5 * S);
                  U = n;
                  var C = Y.YJ();
                  if (C) {
                    var f = g.a1(C, 'X-Client-Wire-Protocol');
                    if (f) {
                      var Q = U.j;
                      !Q.K &&
                        (g.RK(f, 'spdy') || g.RK(f, 'quic') || g.RK(f, 'h2')) &&
                        ((Q.G = Q.J), (Q.K = new Set()), Q.j && (ImX(Q, Q.j), (Q.j = null)));
                    }
                    if (U.rg) {
                      var N = g.a1(C, 'X-HTTP-Session-Id');
                      N && ((U.Cs = N), g.Qp(U.Fk, U.rg, N));
                    }
                  }
                  n.EE = 3;
                  n.J && n.J.MZ();
                  n.eE && (n.uD = Date.now() - Y.jG);
                  U = n;
                  var Z = Y;
                  U.lD = zeQ(U, U.JJ ? U.lN : null, U.CT);
                  if (Z.CG) {
                    gU$(U.j, Z);
                    var T = Z,
                      r = U.dg;
                    r && T.setTimeout(r);
                    T.KG && (heL(T), Bz(T));
                    U.K = Z;
                  } else EUg(U);
                  n.X.length > 0 && x2(n);
                } else (m[0] != 'stop' && m[0] != 'close') || Dl(n, 7);
              else
                n.EE == 3 &&
                  (m[0] == 'stop' || m[0] == 'close'
                    ? m[0] == 'stop'
                      ? Dl(n, 7)
                      : n.disconnect()
                    : m[0] != 'noop' && n.J && n.J.gQ(m),
                  (n.oV = 0));
            }
        jY(4);
      } catch (K) {}
    },
    y6u = function (Y, u) {
      this.K = Y;
      this.map = u;
      this.context = null;
    },
    Vog = function (Y) {
      this.J = Y || 10;
      g.$e.PerformanceNavigationTiming
        ? ((Y = g.$e.performance.getEntriesByType('navigation')),
          (Y = Y.length > 0 && (Y[0].nextHopProtocol == 'hq' || Y[0].nextHopProtocol == 'h2')))
        : (Y = !!(
            g.$e.chrome &&
            g.$e.chrome.loadTimes &&
            g.$e.chrome.loadTimes() &&
            g.$e.chrome.loadTimes().wasFetchedViaSpdy
          ));
      this.G = Y ? this.J : 1;
      this.K = null;
      this.G > 1 && (this.K = new Set());
      this.j = null;
      this.X = [];
    },
    ObJ = function (Y) {
      return Y.j ? !0 : Y.K ? Y.K.size >= Y.G : !1;
    },
    bbu = function (Y) {
      return Y.j ? 1 : Y.K ? Y.K.size : 0;
    },
    WHg = function (Y, u) {
      return Y.j ? Y.j == u : Y.K ? Y.K.has(u) : !1;
    },
    ImX = function (Y, u) {
      Y.K ? Y.K.add(u) : (Y.j = u);
    },
    gU$ = function (Y, u) {
      Y.j && Y.j == u ? (Y.j = null) : Y.K && Y.K.has(u) && Y.K.delete(u);
    },
    FHq = function (Y) {
      if (Y.j != null) return Y.X.concat(Y.j.oV);
      if (Y.K != null && Y.K.size !== 0) {
        var u = Y.X;
        Y = g.A(Y.K.values());
        for (var n = Y.next(); !n.done; n = Y.next()) u = u.concat(n.value.oV);
        return u;
      }
      return g.RL(Y.X);
    },
    J6$ = function (Y, u) {
      var n = new L8();
      if (g.$e.Image) {
        var U = new Image();
        U.onload = g.QC(lE, n, 'TestLoadImage: loaded', !0, u, U);
        U.onerror = g.QC(lE, n, 'TestLoadImage: error', !1, u, U);
        U.onabort = g.QC(lE, n, 'TestLoadImage: abort', !1, u, U);
        U.ontimeout = g.QC(lE, n, 'TestLoadImage: timeout', !1, u, U);
        g.$e.setTimeout(function () {
          if (U.ontimeout) U.ontimeout();
        }, 1e4);
        U.src = Y;
      } else u(!1);
    },
    q2L = function (Y, u) {
      var n = new L8(),
        U = new AbortController(),
        k = setTimeout(function () {
          U.abort();
          lE(n, 'TestPingServer: timeout', !1, u);
        }, 1e4);
      fetch(Y, { signal: U.signal })
        .then(function (m) {
          clearTimeout(k);
          m.ok ? lE(n, 'TestPingServer: ok', !0, u) : lE(n, 'TestPingServer: server error', !1, u);
        })
        .catch(function () {
          clearTimeout(k);
          lE(n, 'TestPingServer: error', !1, u);
        });
    },
    lE = function (Y, u, n, U, k) {
      try {
        (k && ((k.onload = null), (k.onerror = null), (k.onabort = null), (k.ontimeout = null)),
          U(n));
      } catch (m) {}
    },
    am$ = function () {
      this.K = new Ai();
    },
    hi = function (Y, u, n) {
      return n && n.n$ ? n.n$[Y] || u : u;
    },
    $xG = function (Y) {
      this.X = [];
      this.lN =
        this.lD =
        this.Fk =
        this.CT =
        this.K =
        this.Cs =
        this.rg =
        this.MF =
        this.S =
        this.Ru =
        this.N =
          null;
      this.kQ = this.TZ = 0;
      this.gL = hi('failFast', !1, Y);
      this.CG = this.KG = this.Z = this.W = this.J = null;
      this.Qm = !0;
      this.UD = this.zZ = -1;
      this.Gw = this.oV = this.jG = 0;
      this.b8 = hi('baseRetryDelayMs', 5e3, Y);
      this.Jr = hi('retryDelaySeedMs', 1e4, Y);
      this.MA = hi('forwardChannelMaxRetries', 2, Y);
      this.Qe = hi('forwardChannelRequestTimeoutMs', 2e4, Y);
      this.yY = (Y && Y.SFW) || void 0;
      this.SW = (Y && Y.Dxq) || void 0;
      this.sx = (Y && Y.W8g) || !1;
      this.dg = void 0;
      this.JJ = (Y && Y.ybc) || !1;
      this.G = '';
      this.j = new Vog(Y && Y.YAW);
      this.tS = new am$();
      this.Iu = (Y && Y.ObW) || !1;
      this.Uc = (Y && Y.hbF) || !1;
      this.Iu && this.Uc && (this.Uc = !1);
      this.VI = (Y && Y.eOg) || !1;
      Y && Y.AI2 && (this.Qm = !1);
      this.eE = (!this.Iu && this.Qm && Y && Y.tTc) || !1;
      this.MR = void 0;
      Y && Y.lX && Y.lX > 0 && (this.MR = Y.lX);
      this.Ub = void 0;
      this.uD = 0;
      this.Pz = !1;
      this.nT = this.DW = null;
    },
    RO = function (Y) {
      Y.K && (Y$L(Y), Y.K.cancel(), (Y.K = null));
    },
    uQG = function (Y) {
      RO(Y);
      Y.Z && (g.$e.clearTimeout(Y.Z), (Y.Z = null));
      vz(Y);
      Y.j.cancel();
      Y.W && (typeof Y.W === 'number' && g.$e.clearTimeout(Y.W), (Y.W = null));
    },
    x2 = function (Y) {
      ObJ(Y.j) || Y.W || ((Y.W = !0), g.KH(Y.HO, Y), (Y.jG = 0));
    },
    Uy$ = function (Y, u) {
      if (bbu(Y.j) >= Y.j.G - (Y.W ? 1 : 0)) return !1;
      if (Y.W) return ((Y.X = u.oV.concat(Y.X)), !0);
      if (Y.EE == 1 || Y.EE == 2 || Y.jG >= (Y.gL ? 0 : Y.MA)) return !1;
      Y.W = p8((0, g.fR)(Y.HO, Y, u), naC(Y, Y.jG));
      Y.jG++;
      return !0;
    },
    myX = function (Y, u) {
      var n;
      u ? (n = u.CT) : (n = Y.TZ++);
      var U = Y.Fk.clone();
      g.Qp(U, 'SID', Y.G);
      g.Qp(U, 'RID', n);
      g.Qp(U, 'AID', Y.zZ);
      w_(Y, U);
      Y.S && Y.N && g.TL(U, Y.S, Y.N);
      n = new ti(Y, Y.G, n, Y.jG + 1);
      Y.S === null && (n.Fk = Y.N);
      u && (Y.X = u.oV.concat(Y.X));
      u = kCQ(Y, n, 1e3);
      n.setTimeout(Math.round(Y.Qe * 0.5) + Math.round(Y.Qe * 0.5 * Math.random()));
      ImX(Y.j, n);
      BTR(n, U, u);
    },
    w_ = function (Y, u) {
      Y.MF &&
        g.$$(Y.MF, function (n, U) {
          g.Qp(u, U, n);
        });
      Y.J &&
        g.$$({}, function (n, U) {
          g.Qp(u, U, n);
        });
    },
    kCQ = function (Y, u, n) {
      n = Math.min(Y.X.length, n);
      var U = Y.J ? (0, g.fR)(Y.J.Lv, Y.J, Y) : null;
      a: {
        for (var k = Y.X, m = -1; ; ) {
          var X = ['count=' + n];
          m == -1 ? (n > 0 ? ((m = k[0].K), X.push('ofs=' + m)) : (m = 0)) : X.push('ofs=' + m);
          for (var S = !0, C = 0; C < n; C++) {
            var f = k[C].K,
              Q = k[C].map;
            f -= m;
            if (f < 0) ((m = Math.max(0, k[C].K - 100)), (S = !1));
            else
              try {
                f = 'req' + f + '_' || '';
                try {
                  var N = Q instanceof Map ? Q : Object.entries(Q);
                  for (var Z = g.A(N), T = Z.next(); !T.done; T = Z.next()) {
                    var r = g.A(T.value),
                      K = r.next().value,
                      L = r.next().value,
                      R = L;
                    g.XG(L) && (R = g.zE(L));
                    X.push(f + K + '=' + encodeURIComponent(R));
                  }
                } catch (c) {
                  throw (X.push(f + 'type=' + encodeURIComponent('_badmap')), c);
                }
              } catch (c) {
                U && U(Q);
              }
          }
          if (S) {
            N = X.join('&');
            break a;
          }
        }
        N = void 0;
      }
      Y = Y.X.splice(0, n);
      u.oV = Y;
      return N;
    },
    EUg = function (Y) {
      Y.K || Y.Z || ((Y.Gw = 1), g.KH(Y.FQ, Y), (Y.oV = 0));
    },
    eeL = function (Y) {
      if (Y.K || Y.Z || Y.oV >= 3) return !1;
      Y.Gw++;
      Y.Z = p8((0, g.fR)(Y.FQ, Y), naC(Y, Y.oV));
      Y.oV++;
      return !0;
    },
    Y$L = function (Y) {
      Y.DW != null && (g.$e.clearTimeout(Y.DW), (Y.DW = null));
    },
    XFR = function (Y) {
      Y.K = new ti(Y, Y.G, 'rpc', Y.Gw);
      Y.S === null && (Y.K.Fk = Y.N);
      Y.K.dg = 0;
      var u = Y.lD.clone();
      g.Qp(u, 'RID', 'rpc');
      g.Qp(u, 'SID', Y.G);
      g.Qp(u, 'AID', Y.zZ);
      g.Qp(u, 'CI', Y.CG ? '0' : '1');
      !Y.CG && Y.MR && g.Qp(u, 'TO', Y.MR);
      g.Qp(u, 'TYPE', 'xmlhttp');
      w_(Y, u);
      Y.S && Y.N && g.TL(u, Y.S, Y.N);
      Y.dg && Y.K.setTimeout(Y.dg);
      var n = Y.K;
      Y = Y.lN;
      n.JJ = 1;
      n.Z = uE(u.clone());
      n.N = null;
      n.rg = !0;
      tou(n, Y);
    },
    vz = function (Y) {
      Y.KG != null && (g.$e.clearTimeout(Y.KG), (Y.KG = null));
    },
    wkR = function (Y, u) {
      var n = null;
      if (Y.K == u) {
        vz(Y);
        Y$L(Y);
        Y.K = null;
        var U = 2;
      } else if (WHg(Y.j, u)) ((n = u.oV), gU$(Y.j, u), (U = 1));
      else return;
      if (Y.EE != 0)
        if (u.W)
          if (U == 1) {
            n = u.N ? u.N.length : 0;
            u = Date.now() - u.jG;
            var k = Y.jG;
            U = A6C();
            U.dispatchEvent(new pkG(U, n, u, k));
            x2(Y);
          } else EUg(Y);
        else {
          var m = u.Ru;
          k = u.getLastError();
          if (k == 3 || (k == 0 && m > 0) || !((U == 1 && Uy$(Y, u)) || (U == 2 && eeL(Y))))
            switch ((n && n.length > 0 && ((u = Y.j), (u.X = u.X.concat(n))), k)) {
              case 1:
                Dl(Y, 5);
                break;
              case 4:
                Dl(Y, 10);
                break;
              case 3:
                Dl(Y, 6);
                break;
              default:
                Dl(Y, 2);
            }
        }
    },
    naC = function (Y, u) {
      var n = Y.b8 + Math.floor(Math.random() * Y.Jr);
      Y.isActive() || (n *= 2);
      return n * u;
    },
    Dl = function (Y, u) {
      if (u == 2) {
        var n = (0, g.fR)(Y.gQc, Y),
          U = Y.SW,
          k = !U;
        U = new g.UQ(U || '//www.google.com/images/cleardot.gif');
        (g.$e.location && g.$e.location.protocol == 'http') || g.k8(U, 'https');
        uE(U);
        k ? J6$(U.toString(), n) : q2L(U.toString(), n);
      } else K8(2);
      Y.EE = 0;
      Y.J && Y.J.A0(u);
      PUy(Y);
      uQG(Y);
    },
    PUy = function (Y) {
      Y.EE = 0;
      Y.nT = [];
      if (Y.J) {
        var u = FHq(Y.j);
        if (u.length != 0 || Y.X.length != 0)
          (g.DJ(Y.nT, u), g.DJ(Y.nT, Y.X), (Y.j.X.length = 0), g.RL(Y.X), (Y.X.length = 0));
        Y.J.WO();
      }
    },
    S$G = function (Y) {
      if (Y.EE == 0) return Y.nT;
      var u = [];
      g.DJ(u, FHq(Y.j));
      g.DJ(u, Y.X);
      return u;
    },
    zeQ = function (Y, u, n) {
      var U = g.Ns(n);
      U.K != ''
        ? (u && g.mJ(U, u + '.' + U.K), g.XD(U, U.X))
        : ((U = g.$e.location),
          (U = ZvG(U.protocol, u ? u + '.' + U.hostname : U.hostname, +U.port, n)));
      u = Y.rg;
      n = Y.Cs;
      u && n && g.Qp(U, u, n);
      g.Qp(U, 'VER', Y.OB);
      w_(Y, U);
      return U;
    },
    oUC = function (Y, u, n) {
      if (u && !Y.JJ) throw Error("Can't create secondary domain capable XhrIo object.");
      u = Y.sx && !Y.yY ? new g.HB(new g.$W({ CV: n })) : new g.HB(Y.yY);
      u.S = Y.JJ;
      return u;
    },
    CU$ = function () {},
    f0X = function () {},
    eY = function (Y, u) {
      g.is.call(this);
      this.K = new $xG(u);
      this.J = Y;
      this.j = (u && u.jVW) || null;
      Y = (u && u.bGV) || null;
      u &&
        u.T_V &&
        (Y ? (Y['X-Client-Protocol'] = 'webchannel') : (Y = { 'X-Client-Protocol': 'webchannel' }));
      this.K.N = Y;
      Y = (u && u.dea) || null;
      u &&
        u.pH &&
        (Y ? (Y['X-WebChannel-Content-Type'] = u.pH) : (Y = { 'X-WebChannel-Content-Type': u.pH }));
      u &&
        u.vn &&
        (Y
          ? (Y['X-WebChannel-Client-Profile'] = u.vn)
          : (Y = { 'X-WebChannel-Client-Profile': u.vn }));
      this.K.Ru = Y;
      (Y = u && u.ExJ) && !g.vq(Y) && (this.K.S = Y);
      this.W = (u && u.ybc) || !1;
      this.G = (u && u.YGw) || !1;
      (u = u && u.tF) &&
        !g.vq(u) &&
        ((this.K.rg = u), g.f3(this.j, u) && ((Y = this.j), u in Y && delete Y[u]));
      this.X = new Wz(this);
    },
    QRX = function (Y) {
      sUg.call(this);
      Y.__headers__ &&
        ((this.headers = Y.__headers__),
        (this.statusCode = Y.__status__),
        delete Y.__headers__,
        delete Y.__status__);
      var u = Y.__sm__;
      u ? (this.data = (this.K = g.UF(u)) ? g.Zn(u, this.K) : u) : (this.data = Y);
    },
    NDg = function (Y) {
      dxX.call(this);
      this.status = 1;
      this.errorCode = Y;
    },
    Wz = function (Y) {
      this.K = Y;
    },
    iXg = function (Y, u) {
      this.j = Y;
      this.K = u;
    },
    ZXG = function (Y) {
      return S$G(Y.K).map(function (u) {
        var n = Y.j;
        u = u.map;
        '__data__' in u ? ((u = u.__data__), (n = n.G ? XyB(u) : u)) : (n = u);
        return n;
      });
    },
    bE = function (Y, u) {
      if (typeof Y !== 'function') throw Error('Fn must not be null and must be a function');
      return g.$e.setTimeout(function () {
        Y();
      }, u);
    },
    zx = function (Y) {
      IO.dispatchEvent(new TDJ(IO, Y));
    },
    TDJ = function (Y) {
      g.Vy.call(this, 'statevent', Y);
    },
    g_ = function (Y, u, n, U) {
      this.K = Y;
      this.G = u;
      this.S = n;
      this.W = U || 1;
      this.j = 45e3;
      this.X = new g.rH(this);
      this.J = new g.wr();
      this.J.setInterval(250);
    },
    M2g = function (Y, u, n) {
      Y.QU = 1;
      Y.xP = uE(u.clone());
      Y.Yq = n;
      Y.rg = !0;
      rEg(Y, null);
    },
    sRB = function (Y, u, n, U, k) {
      Y.QU = 1;
      Y.xP = uE(u.clone());
      Y.Yq = null;
      Y.rg = n;
      k && (Y.a$ = !1);
      rEg(Y, U);
    },
    rEg = function (Y, u) {
      Y.oQ = Date.now();
      dyX(Y);
      Y.B6 = Y.xP.clone();
      n8(Y.B6, 't', Y.W);
      Y.eX = 0;
      Y.fU = Y.K.vU(Y.K.fM() ? u : null);
      Y.Tb > 0 && (Y.kh = new g.qs((0, g.fR)(Y.J0, Y, Y.fU), Y.Tb));
      Y.X.listen(Y.fU, 'readystatechange', Y.Fv);
      u = Y.zN ? g.rc(Y.zN) : {};
      Y.Yq
        ? ((Y.Z5 = 'POST'),
          (u['Content-Type'] = 'application/x-www-form-urlencoded'),
          Y.fU.send(Y.B6, Y.Z5, Y.Yq, u))
        : ((Y.Z5 = 'GET'),
          Y.a$ && !g.NK && (u.Connection = 'close'),
          Y.fU.send(Y.B6, Y.Z5, null, u));
      Y.K.Sn(1);
    },
    jRu = function (Y, u) {
      var n = Y.eX,
        U = u.indexOf('\n', n);
      if (U == -1) return GC$;
      n = Number(u.substring(n, U));
      if (isNaN(n)) return AEX;
      U += 1;
      if (U + n > u.length) return GC$;
      u = u.slice(U, U + n);
      Y.eX = U + n;
      return u;
    },
    dyX = function (Y) {
      Y.YF = Date.now() + Y.j;
      Kh$(Y, Y.j);
    },
    Kh$ = function (Y, u) {
      if (Y.O7 != null) throw Error('WatchDog timer not null');
      Y.O7 = bE((0, g.fR)(Y.OM, Y), u);
    },
    pFy = function (Y) {
      Y.O7 && (g.$e.clearTimeout(Y.O7), (Y.O7 = null));
    },
    LhR = function (Y) {
      Y.K.cW() || Y.IQ || Y.K.mH(Y);
    },
    E1 = function (Y) {
      pFy(Y);
      g.nc(Y.kh);
      Y.kh = null;
      Y.J.stop();
      Y.X.removeAll();
      if (Y.fU) {
        var u = Y.fU;
        Y.fU = null;
        u.abort();
        u.dispose();
      }
      Y.Rd && (Y.Rd = null);
    },
    t2G = function (Y, u) {
      try {
        (Y.K.Vo(Y, u), Y.K.Sn(4));
      } catch (n) {}
    },
    oaR = function (Y, u, n, U, k) {
      if (U == 0) n(!1);
      else {
        var m = k || 0;
        U--;
        BDC(Y, u, function (X) {
          X
            ? n(!0)
            : g.$e.setTimeout(function () {
                oaR(Y, u, n, U, m);
              }, m);
        });
      }
    },
    BDC = function (Y, u, n) {
      var U = new Image();
      U.onload = function () {
        try {
          (Hz(U), n(!0));
        } catch (k) {}
      };
      U.onerror = function () {
        try {
          (Hz(U), n(!1));
        } catch (k) {}
      };
      U.onabort = function () {
        try {
          (Hz(U), n(!1));
        } catch (k) {}
      };
      U.ontimeout = function () {
        try {
          (Hz(U), n(!1));
        } catch (k) {}
      };
      g.$e.setTimeout(function () {
        if (U.ontimeout) U.ontimeout();
      }, u);
      U.src = Y;
    },
    Hz = function (Y) {
      Y.onload = null;
      Y.onerror = null;
      Y.onabort = null;
      Y.ontimeout = null;
    },
    cE$ = function (Y) {
      this.K = Y;
      this.j = new Ai();
    },
    va$ = function (Y) {
      var u = yo(Y.K, Y.Un, '/mail/images/cleardot.gif');
      uE(u);
      oaR(u.toString(), 5e3, (0, g.fR)(Y.t5, Y), 3, 2e3);
      Y.Sn(1);
    },
    R3$ = function (Y) {
      var u = Y.K.W;
      u != null
        ? (zx(5), u ? (zx(11), Vo(Y.K, Y, !1)) : (zx(12), Vo(Y.K, Y, !0)))
        : ((Y.sT = new g_(Y)),
          (Y.sT.zN = Y.PU),
          (u = Y.K),
          (u = yo(u, u.fM() ? Y.Ew : null, Y.sL)),
          zx(5),
          n8(u, 'TYPE', 'xmlhttp'),
          sRB(Y.sT, u, !1, Y.Ew, !1));
    },
    Dyy = function (Y, u, n) {
      this.K = 1;
      this.j = [];
      this.X = [];
      this.J = new Ai();
      this.N = Y || null;
      this.W = u != null ? u : null;
      this.Z = n || !1;
    },
    xyL = function (Y, u) {
      this.K = Y;
      this.map = u;
      this.context = null;
    },
    l0G = function (Y, u, n, U) {
      g.Vy.call(this, 'timingevent', Y);
      this.size = u;
      this.rtt = n;
      this.retries = U;
    },
    h3C = function (Y) {
      g.Vy.call(this, 'serverreachability', Y);
    },
    Whu = function (Y) {
      Y.HE(1, 0);
      Y.d4 = yo(Y, null, Y.UL);
      wFu(Y);
    },
    e3$ = function (Y) {
      Y.wu && (Y.wu.abort(), (Y.wu = null));
      Y.PW && (Y.PW.cancel(), (Y.PW = null));
      Y.wM && (g.$e.clearTimeout(Y.wM), (Y.wM = null));
      O1(Y);
      Y.Rm && (Y.Rm.cancel(), (Y.Rm = null));
      Y.WS && (g.$e.clearTimeout(Y.WS), (Y.WS = null));
    },
    bXR = function (Y, u) {
      if (Y.K == 0) throw Error('Invalid operation: sending map when state is closed');
      Y.j.push(new xyL(Y.WE++, u));
      (Y.K != 2 && Y.K != 3) || wFu(Y);
    },
    I0B = function (Y) {
      var u = 0;
      Y.PW && u++;
      Y.Rm && u++;
      return u;
    },
    wFu = function (Y) {
      Y.Rm || Y.WS || ((Y.WS = bE((0, g.fR)(Y.im, Y), 0)), (Y.Hy = 0));
    },
    EaR = function (Y, u) {
      if (Y.K == 1) {
        if (!u) {
          Y.nM = Math.floor(Math.random() * 1e5);
          u = Y.nM++;
          var n = new g_(Y, '', u);
          n.zN = Y.d3;
          var U = z3R(Y),
            k = Y.d4.clone();
          g.Qp(k, 'RID', u);
          g.Qp(k, 'CVER', '1');
          FP(Y, k);
          M2g(n, k, U);
          Y.Rm = n;
          Y.K = 2;
        }
      } else Y.K == 3 && (u ? ga$(Y, u) : Y.j.length == 0 || Y.Rm || ga$(Y));
    },
    ga$ = function (Y, u) {
      if (u)
        if (Y.vL > 6) {
          Y.j = Y.X.concat(Y.j);
          Y.X.length = 0;
          var n = Y.nM - 1;
          u = z3R(Y);
        } else ((n = u.S), (u = u.Yq));
      else ((n = Y.nM++), (u = z3R(Y)));
      var U = Y.d4.clone();
      g.Qp(U, 'SID', Y.G);
      g.Qp(U, 'RID', n);
      g.Qp(U, 'AID', Y.Wy);
      FP(Y, U);
      n = new g_(Y, Y.G, n, Y.Hy + 1);
      n.zN = Y.d3;
      n.setTimeout(1e4 + Math.round(1e4 * Math.random()));
      Y.Rm = n;
      M2g(n, U, u);
    },
    FP = function (Y, u) {
      Y.dw &&
        (Y = Y.dw.eF()) &&
        g.$$(Y, function (n, U) {
          g.Qp(u, U, n);
        });
    },
    z3R = function (Y) {
      var u = Math.min(Y.j.length, 1e3),
        n = ['count=' + u];
      if (Y.vL > 6 && u > 0) {
        var U = Y.j[0].K;
        n.push('ofs=' + U);
      } else U = 0;
      for (var k = {}, m = 0; m < u; k = { hQ: void 0 }, m++) {
        k.hQ = Y.j[m].K;
        var X = Y.j[m].map;
        k.hQ = Y.vL <= 6 ? m : k.hQ - U;
        try {
          g.$$(
            X,
            (function (S) {
              return function (C, f) {
                n.push('req' + S.hQ + '_' + f + '=' + encodeURIComponent(C));
              };
            })(k)
          );
        } catch (S) {
          n.push('req' + k.hQ + '_type=' + encodeURIComponent('_badmap'));
        }
      }
      Y.X = Y.X.concat(Y.j.splice(0, u));
      return n.join('&');
    },
    HX$ = function (Y) {
      Y.PW || Y.wM || ((Y.S = 1), (Y.wM = bE((0, g.fR)(Y.lm, Y), 0)), (Y.Fb = 0));
    },
    V2Q = function (Y) {
      if (Y.PW || Y.wM || Y.Fb >= 3) return !1;
      Y.S++;
      Y.wM = bE((0, g.fR)(Y.lm, Y), yE$(Y, Y.Fb));
      Y.Fb++;
      return !0;
    },
    Vo = function (Y, u, n) {
      Y.Mv = Y.W == null ? n : !Y.W;
      Y.fd = u.dM;
      Y.Z || Whu(Y);
    },
    O1 = function (Y) {
      Y.PL != null && (g.$e.clearTimeout(Y.PL), (Y.PL = null));
    },
    yE$ = function (Y, u) {
      var n = 5e3 + Math.floor(Math.random() * 1e4);
      Y.isActive() || (n *= 2);
      return n * u;
    },
    Ji = function (Y, u) {
      if (u == 2 || u == 9) {
        var n = null;
        Y.dw && (n = null);
        var U = (0, g.fR)(Y.Abq, Y);
        n || ((n = new g.UQ('//www.google.com/images/cleardot.gif')), uE(n));
        BDC(n.toString(), 1e4, U);
      } else zx(2);
      OX$(Y, u);
    },
    OX$ = function (Y, u) {
      Y.K = 0;
      Y.dw && Y.dw.kN(u);
      FhX(Y);
      e3$(Y);
    },
    FhX = function (Y) {
      Y.K = 0;
      Y.fd = -1;
      if (Y.dw)
        if (Y.X.length == 0 && Y.j.length == 0) Y.dw.Nv();
        else {
          var u = g.RL(Y.X),
            n = g.RL(Y.j);
          Y.X.length = 0;
          Y.j.length = 0;
          Y.dw.Nv(u, n);
        }
    },
    yo = function (Y, u, n) {
      var U = g.Ns(n);
      if (U.K != '') (u && g.mJ(U, u + '.' + U.K), g.XD(U, U.X));
      else {
        var k = window.location;
        U = ZvG(k.protocol, u ? u + '.' + k.hostname : k.hostname, +k.port, n);
      }
      Y.RQ &&
        g.$$(Y.RQ, function (m, X) {
          g.Qp(U, X, m);
        });
      g.Qp(U, 'VER', Y.vL);
      FP(Y, U);
      return U;
    },
    JE$ = function () {},
    q$$ = function () {
      this.K = [];
      this.j = [];
    },
    a0q = function (Y) {
      g.Vy.call(this, 'channelMessage');
      this.message = Y;
    },
    $yg = function (Y) {
      g.Vy.call(this, 'channelError');
      this.error = Y;
    },
    Y0B = function (Y, u) {
      this.action = Y;
      this.params = u || {};
    },
    qC = function (Y, u) {
      g.e.call(this);
      this.K = new g.Vp(this.bsG, 0, this);
      g.b(this, this.K);
      this.Qu = 5e3;
      this.j = 0;
      if (typeof Y === 'function') u && (Y = (0, g.fR)(Y, u));
      else if (Y && typeof Y.handleEvent === 'function') Y = (0, g.fR)(Y.handleEvent, Y);
      else throw Error('Invalid listener argument');
      this.X = Y;
    },
    uu$ = function (Y, u, n, U, k, m, X, S, C, f, Q, N, Z, T) {
      n = n === void 0 ? !1 : n;
      U =
        U === void 0
          ? function () {
              return '';
            }
          : U;
      k = k === void 0 ? !1 : k;
      m = m === void 0 ? !1 : m;
      X = X === void 0 ? !1 : X;
      S =
        S === void 0
          ? function () {
              return g.R1({});
            }
          : S;
      C = C === void 0 ? !1 : C;
      Q = Q === void 0 ? !1 : Q;
      N = N === void 0 ? !1 : N;
      Z = Z === void 0 ? !1 : Z;
      T = T === void 0 ? !1 : T;
      this.JJ = Y;
      this.KG = u;
      this.W = new g.KE();
      this.j = new qC(this.VWa, this);
      this.K = null;
      this.S = !1;
      this.N = null;
      this.jG = '';
      this.oV = this.Z = 0;
      this.X = [];
      this.Gw = n;
      this.rg = U;
      this.J = m;
      this.Fk = S;
      this.MF = f;
      this.lN = X;
      this.DW = null;
      this.G = g.R1();
      this.CT = k;
      this.nT = C;
      this.Iu = Q;
      this.Uc = N;
      this.Qm = Z;
      this.Ru = T;
      this.dg = new PL$();
      this.CG = new SUL();
      this.Pz = new fzL();
      this.TZ = new CLX();
      this.zZ = new QoX();
      this.eE = new NLR();
      this.Ub = new ivJ();
    },
    kl$ = function (Y, u, n, U, k) {
      nHQ(Y);
      if (Y.K) {
        var m = g.z6('ID_TOKEN'),
          X = Y.K.d3 || {};
        m ? (X['x-youtube-identity-token'] = m) : delete X['x-youtube-identity-token'];
        Y.K.d3 = X;
      }
      U3R(Y);
      U
        ? ((U.getState() != 3 && I0B(U) == 0) || U.getState(), Y.K.connect(u, n, Y.KG, U.G, U.Wy))
        : k
          ? Y.K.connect(u, n, Y.KG, k.sessionId, k.arrayId)
          : Y.K.connect(u, n, Y.KG);
    },
    S0q = function (Y, u) {
      return Y.Qm
        ? !0
        : Y.Uc
          ? Object.values(m3q).includes(u)
          : Y.Iu
            ? !Object.values(XNy).includes(u)
            : Y.Ru
              ? Object.values(PDX).includes(u)
              : !1;
    },
    Q9$ = function (Y) {
      var u, n;
      g.l(function (U) {
        if (U.j == 1) return (g.LY(U, 2), g.D(U, CD$(Y), 2));
        g.lB(U);
        u = Y.X;
        Y.X = [];
        n = u.length;
        fX$(Y, u, n);
        aO(Y);
        return g.wG(U, 0);
      });
    },
    fX$ = function (Y, u, n) {
      for (var U = 0; U < n; ++U) bXR(Y.K, u[U]);
      aO(Y);
    },
    aO = function (Y) {
      Y.publish('handlerOpened');
      Y.dg.i8('BROWSER_CHANNEL');
    },
    nHQ = function (Y) {
      if (Y.K) {
        var u = Y.rg(),
          n = Y.K.d3 || {};
        u ? (n['x-youtube-lounge-xsrf-token'] = u) : delete n['x-youtube-lounge-xsrf-token'];
        Y.K.d3 = n;
      }
    },
    CD$ = function (Y) {
      if (Y.nT) return g.R1();
      if (!Y.lN) return NoL(Y);
      Y.DW === null && (Y.DW = NoL(Y));
      return Y.DW;
    },
    NoL = function (Y) {
      return g.ls(
        Y.Fk()
          .then(function (u) {
            izg(Y, u);
          })
          .Qg(function () {}),
        function () {
          Y.DW = null;
        }
      );
    },
    izg = function (Y, u) {
      if (Y.K) {
        var n = Y.K.d3 || {};
        u && Object.keys(u).length > 0 ? (n = Object.assign({}, n, u)) : delete n.Authorization;
        Y.K.d3 = n;
      }
    },
    U3R = function (Y) {
      Y.MF && !Y.J && izg(Y, Y.MF());
    },
    $2 = function (Y) {
      this.scheme = 'https';
      this.port = this.domain = '';
      this.K = '/api/lounge';
      this.j = !0;
      Y = Y || document.location.href;
      var u = Number(g.Co(Y)[4] || null) || '';
      u && (this.port = ':' + u);
      this.domain = g.fo(Y) || '';
      Y = g.Wq();
      Y.search('MSIE') >= 0 &&
        ((Y = Y.match(/MSIE ([\d.]+)/)[1]), g.wc(Y, '10.0') < 0 && (this.j = !1));
    },
    Yt = function (Y, u) {
      var n = Y.K;
      Y.j && (n = Y.scheme + '://' + Y.domain + Y.port + Y.K);
      return g.Mk(n + u, {});
    },
    ZzX = function (Y, u) {
      g.is.call(this);
      var n = this;
      this.P0 = Y();
      this.P0.subscribe('handlerOpened', this.gT, this);
      this.P0.subscribe('handlerClosed', this.onClosed, this);
      this.P0.subscribe('handlerError', function (U, k) {
        n.onError(k);
      });
      this.P0.subscribe('handlerMessage', this.onMessage, this);
      this.K = u;
    },
    Toy = function (Y, u, n) {
      var U = this;
      n =
        n === void 0
          ? function () {
              return '';
            }
          : n;
      var k = k === void 0 ? new f0X() : k;
      var m = m === void 0 ? new g.KE() : m;
      this.pathPrefix = Y;
      this.K = u;
      this.jG = n;
      this.J = m;
      this.Z = null;
      this.N = this.S = 0;
      this.channel = null;
      this.W = 0;
      this.X = new qC(function () {
        U.X.isActive();
        var X;
        ((X = U.channel) == null ? void 0 : bbu(new iXg(X, X.K).K.j)) === 0 && U.connect(U.Z, U.S);
      });
      this.G = {};
      this.j = {};
      this.KG = !1;
      this.logger = null;
      this.oV = [];
      this.Ab = void 0;
      this.Fk = new PL$();
      this.DW = new SUL();
      this.MF = new CLX();
      this.rg = new QoX();
    },
    rDu = function (Y) {
      g.us(Y.channel, 'm', function () {
        Y.W = 3;
        Y.X.reset();
        Y.Z = null;
        Y.S = 0;
        for (var u = g.A(Y.oV), n = u.next(); !n.done; n = u.next())
          ((n = n.value), Y.channel && Y.channel.send(n));
        Y.oV = [];
        Y.publish('webChannelOpened');
        Y.Fk.i8('WEB_CHANNEL');
      });
      g.us(Y.channel, 'n', function () {
        Y.W = 0;
        Y.X.isActive() || Y.publish('webChannelClosed');
        var u,
          n = (u = Y.channel) == null ? void 0 : ZXG(new iXg(u, u.K));
        n && (Y.oV = [].concat(g.Zu(n)));
        Y.DW.i8('WEB_CHANNEL');
      });
      g.us(Y.channel, 'p', function (u) {
        var n = u.data;
        n[0] === 'gracefulReconnect'
          ? (Y.X.start(), Y.channel && Y.channel.close())
          : Y.publish('webChannelMessage', new Y0B(n[0], n[1]));
        Y.Ab = u.statusCode;
        Y.MF.i8('WEB_CHANNEL');
      });
      g.us(Y.channel, 'o', function () {
        Y.Ab === 401 || Y.X.start();
        Y.publish('webChannelError');
        Y.rg.i8('WEB_CHANNEL', '');
      });
    },
    Mvg = function (Y) {
      var u = Y.jG();
      u ? (Y.G['x-youtube-lounge-xsrf-token'] = u) : delete Y.G['x-youtube-lounge-xsrf-token'];
    },
    s9L = function (Y) {
      g.is.call(this);
      this.K = Y();
      this.K.subscribe('webChannelOpened', this.Mu, this);
      this.K.subscribe('webChannelClosed', this.onClosed, this);
      this.K.subscribe('webChannelError', this.onError, this);
      this.K.subscribe('webChannelMessage', this.onMessage, this);
    },
    d3C = function (Y, u, n, U, k) {
      function m() {
        return new uu$(Yt(Y, '/bc'), u, !1, n, U);
      }
      n =
        n === void 0
          ? function () {
              return '';
            }
          : n;
      return g.rL('enable_mdx_web_channel_desktop')
        ? new s9L(function () {
            return new Toy(Yt(Y, '/wc'), u, n);
          })
        : new ZzX(m, k);
    },
    KKR = function () {
      var Y = GlR;
      ADL();
      ui.push(Y);
      j9L();
    },
    ne = function (Y, u) {
      ADL();
      var n = pNR(Y, String(u));
      ui.length == 0
        ? LKB(n)
        : (j9L(),
          g.Jy(ui, function (U) {
            U(n);
          }));
    },
    UI = function (Y) {
      ne('CP', Y);
    },
    ADL = function () {
      ui ||
        ((ui = g.nR('yt.mdx.remote.debug.handlers_') || []),
        g.Y$('yt.mdx.remote.debug.handlers_', ui));
    },
    LKB = function (Y) {
      var u = (kt + 1) % 50;
      kt = u;
      mY[u] = Y;
      Xm || (Xm = u == 49);
    },
    j9L = function () {
      var Y = ui;
      if (mY[0]) {
        var u = Xm ? kt : -1,
          n = {};
        do
          ((n = { F9: void 0 }),
            (u = (u + 1) % 50),
            (n.F9 = mY[u]),
            g.Jy(
              Y,
              (function (U) {
                return function (k) {
                  k(U.F9);
                };
              })(n)
            ));
        while (u != kt);
        mY = Array(50);
        kt = -1;
        Xm = !1;
      }
    },
    pNR = function (Y, u) {
      var n = (Date.now() - tvy) / 1e3;
      n.toFixed && (n = n.toFixed(3));
      var U = [];
      U.push('[', n + 's', '] ');
      U.push('[', 'yt.mdx.remote', '] ');
      U.push(Y + ': ' + u, '\n');
      return U.join('');
    },
    Ps = function (Y) {
      g.ud.call(this);
      this.W = Y;
      this.screens = [];
    },
    BoR = function (Y, u) {
      var n = Y.get(u.uuid) || Y.get(u.id);
      if (n)
        return (
          (Y = n.name),
          (n.id = u.id || n.id),
          (n.name = u.name),
          (n.token = u.token),
          (n.uuid = u.uuid || n.uuid),
          n.name != Y
        );
      Y.screens.push(u);
      return !0;
    },
    oHu = function (Y, u) {
      var n = Y.screens.length != u.length;
      Y.screens = g.BV(Y.screens, function (m) {
        return !!VsL(u, m);
      });
      for (var U = u.length, k = 0; k < U; k++) n = BoR(Y, u[k]) || n;
      return n;
    },
    cDq = function (Y, u) {
      var n = Y.screens.length;
      Y.screens = g.BV(Y.screens, function (U) {
        return !(U || u ? (!U != !u ? 0 : U.id == u.id) : 1);
      });
      return Y.screens.length < n;
    },
    vH$ = function (Y, u, n, U, k) {
      g.ud.call(this);
      this.X = Y;
      this.S = u;
      this.G = n;
      this.W = U;
      this.J = k;
      this.j = 0;
      this.K = null;
      this.C0 = NaN;
    },
    Ce = function (Y) {
      Ps.call(this, 'LocalScreenService');
      this.j = Y;
      this.K = NaN;
      SQ(this);
      this.info('Initializing with ' + EoX(this.screens));
    },
    RN$ = function (Y) {
      if (Y.screens.length) {
        var u = g.dA(Y.screens, function (U) {
            return U.id;
          }),
          n = Yt(Y.j, '/pairing/get_lounge_token_batch');
        Y.j.sendRequest(
          'POST',
          n,
          { screen_ids: u.join(',') },
          (0, g.fR)(Y.O9, Y),
          (0, g.fR)(Y.L8, Y)
        );
      }
    },
    SQ = function (Y) {
      if (g.rL('deprecate_pair_servlet_enabled')) return oHu(Y, []);
      var u = goG(Y2g());
      u = g.BV(u, function (n) {
        return !n.uuid;
      });
      return oHu(Y, u);
    },
    fe = function (Y, u) {
      nUq(g.dA(Y.screens, joy));
      u && uJ$();
    },
    x3$ = function (Y, u) {
      g.ud.call(this);
      this.W = u;
      u = (u = g.ck('yt-remote-online-screen-ids') || '') ? u.split(',') : [];
      for (var n = {}, U = this.W(), k = U.length, m = 0; m < k; ++m) {
        var X = U[m].id;
        n[X] = g.jB(u, X);
      }
      this.K = n;
      this.J = Y;
      this.X = this.G = NaN;
      this.j = null;
      D3J('Initialized with ' + g.zE(this.K));
    },
    lX$ = function (Y, u, n) {
      var U = Yt(Y.J, '/pairing/get_screen_availability');
      Y.J.sendRequest(
        'POST',
        U,
        { lounge_token: u.token },
        (0, g.fR)(function (k) {
          k = k.screens || [];
          for (var m = k.length, X = 0; X < m; ++X)
            if (k[X].loungeToken == u.token) {
              n(k[X].status == 'online');
              return;
            }
          n(!1);
        }, Y),
        (0, g.fR)(function () {
          n(!1);
        }, Y)
      );
    },
    wN$ = function (Y, u) {
      a: if (kqX(u) != kqX(Y.K)) var n = !1;
      else {
        n = g.C3(u);
        for (var U = n.length, k = 0; k < U; ++k)
          if (!Y.K[n[k]]) {
            n = !1;
            break a;
          }
        n = !0;
      }
      n || (D3J('Updated online screens: ' + g.zE(Y.K)), (Y.K = u), Y.publish('screenChange'));
      hNR(Y);
    },
    Q5 = function (Y) {
      isNaN(Y.X) || g.iL(Y.X);
      Y.X = g.QS((0, g.fR)(Y.mA, Y), Y.G > 0 && Y.G < g.iQ() ? 2e4 : 1e4);
    },
    D3J = function (Y) {
      ne('OnlineScreenService', Y);
    },
    WKq = function (Y) {
      var u = {};
      g.Jy(Y.W(), function (n) {
        n.token
          ? (u[n.token] = n.id)
          : this.nk('Requesting availability of screen w/o lounge token.');
      });
      return u;
    },
    hNR = function (Y) {
      Y = g.C3(
        g.YP(Y.K, function (u) {
          return u;
        })
      );
      g.VC(Y);
      Y.length
        ? g.oU('yt-remote-online-screen-ids', Y.join(','), 60)
        : g.vk('yt-remote-online-screen-ids');
    },
    Nh = function (Y, u) {
      u = u === void 0 ? !1 : u;
      Ps.call(this, 'ScreenService');
      this.G = Y;
      this.S = u;
      this.K = this.j = null;
      this.X = [];
      this.J = {};
      eNR(this);
    },
    IXJ = function (Y, u, n, U, k, m) {
      Y.info('getAutomaticScreenByIds ' + n + ' / ' + u);
      n || (n = Y.J[u]);
      var X = Y.XS(),
        S = n ? NC(X, n) : null;
      (n && (Y.S || S)) || (S = NC(X, u));
      if (S) {
        S.uuid = u;
        var C = ii(Y, S);
        lX$(Y.K, C, function (f) {
          k(f ? C : null);
        });
      } else
        n
          ? bzR(
              Y,
              n,
              (0, g.fR)(function (f) {
                var Q = ii(this, new C8({ name: U, screenId: n, loungeToken: f, dialId: u || '' }));
                lX$(this.K, Q, function (N) {
                  k(N ? Q : null);
                });
              }, Y),
              m
            )
          : k(null);
    },
    zN$ = function (Y, u) {
      for (var n = Y.screens.length, U = 0; U < n; ++U)
        if (Y.screens[U].name == u) return Y.screens[U];
      return null;
    },
    gHR = function (Y, u, n) {
      lX$(Y.K, u, n);
    },
    bzR = function (Y, u, n, U) {
      Y.info('requestLoungeToken_ for ' + u);
      var k = {
        postParams: { screen_ids: u },
        method: 'POST',
        context: Y,
        onSuccess: function (m, X) {
          m = (X && X.screens) || [];
          m[0] && m[0].screenId == u
            ? n(m[0].loungeToken)
            : U(Error('Missing lounge token in token response'));
        },
        onError: function () {
          U(Error('Request screen lounge token failed'));
        },
      };
      g.Ak(Yt(Y.G, '/pairing/get_lounge_token_batch'), k);
    },
    EHG = function (Y) {
      Y.screens = Y.j.XS();
      var u = Y.J,
        n = {},
        U;
      for (U in u) n[u[U]] = U;
      u = Y.screens.length;
      for (U = 0; U < u; ++U) {
        var k = Y.screens[U];
        k.uuid = n[k.id] || '';
      }
      Y.info('Updated manual screens: ' + EoX(Y.screens));
    },
    eNR = function (Y) {
      Hzy(Y);
      Y.j = new Ce(Y.G);
      Y.j.subscribe('screenChange', (0, g.fR)(Y.C8, Y));
      EHG(Y);
      Y.S || (Y.X = goG(g.ck('yt-remote-automatic-screen-cache') || []));
      Hzy(Y);
      Y.info('Initializing automatic screens: ' + EoX(Y.X));
      Y.K = new x3$(Y.G, (0, g.fR)(Y.XS, Y, !0));
      Y.K.subscribe(
        'screenChange',
        (0, g.fR)(function () {
          this.publish('onlineScreenChange');
        }, Y)
      );
    },
    ii = function (Y, u) {
      var n = Y.get(u.id);
      n
        ? ((n.uuid = u.uuid), (u = n))
        : ((n = NC(Y.X, u.uuid)) ? ((n.id = u.id), (n.token = u.token), (u = n)) : Y.X.push(u),
          Y.S || yDR(Y));
      Hzy(Y);
      Y.J[u.uuid] = u.id;
      g.oU('yt-remote-device-id-map', Y.J, 31536e3);
      return u;
    },
    yDR = function (Y) {
      Y = g.BV(Y.X, function (u) {
        return u.idType != 'shortLived';
      });
      g.oU('yt-remote-automatic-screen-cache', g.dA(Y, joy));
    },
    Hzy = function (Y) {
      Y.J = g.ck('yt-remote-device-id-map') || {};
    },
    ZQ = function (Y, u, n) {
      g.ud.call(this);
      this.rg = n;
      this.G = Y;
      this.j = u;
      this.K = null;
    },
    TM = function (Y, u) {
      Y.K = u;
      Y.publish('sessionScreen', Y.K);
    },
    VvR = function (Y, u) {
      Y.K && ((Y.K.token = u), ii(Y.G, Y.K));
      Y.publish('sessionScreen', Y.K);
    },
    r1 = function (Y, u) {
      ne(Y.rg, u);
    },
    Mh = function (Y, u, n) {
      ZQ.call(this, Y, u, 'CastSession');
      var U = this;
      this.config_ = n;
      this.X = null;
      this.oV = (0, g.fR)(this.lj, this);
      this.DW = (0, g.fR)(this.WI2, this);
      this.KG = g.QS(function () {
        Ozy(U, null);
      }, 12e4);
      this.S = this.J = this.W = this.Z = 0;
      this.jG = !1;
      this.N = 'unknown';
    },
    JDB = function (Y, u) {
      g.iL(Y.S);
      Y.S = 0;
      u == 0
        ? FKL(Y)
        : (Y.S = g.QS(function () {
            FKL(Y);
          }, u));
    },
    FKL = function (Y) {
      q0$(Y, 'getLoungeToken');
      g.iL(Y.J);
      Y.J = g.QS(function () {
        aXL(Y, null);
      }, 3e4);
    },
    q0$ = function (Y, u) {
      Y.info('sendYoutubeMessage_: ' + u + ' ' + g.zE());
      var n = {};
      n.type = u;
      Y.X
        ? Y.X.sendMessage(
            'urn:x-cast:com.google.youtube.mdx',
            n,
            function () {},
            (0, g.fR)(function () {
              r1(this, 'Failed to send message: ' + u + '.');
            }, Y)
          )
        : r1(Y, 'Sending yt message without session: ' + g.zE(n));
    },
    $3Q = function (Y, u) {
      u
        ? (Y.info('onConnectedScreenId_: Received screenId: ' + u),
          (Y.K && Y.K.id == u) ||
            Y.X8(
              u,
              function (n) {
                TM(Y, n);
              },
              function () {
                return Y.gO();
              },
              5
            ))
        : Y.gO(Error('Waiting for session status timed out.'));
    },
    up$ = function (Y, u, n) {
      Y.info('onConnectedScreenData_: Received screenData: ' + JSON.stringify(u));
      var U = new C8(u);
      YLC(
        Y,
        U,
        function (k) {
          k
            ? ((Y.jG = !0), ii(Y.G, U), TM(Y, U), (Y.N = 'unknown'), JDB(Y, n))
            : (g.VM(
                Error(
                  'CastSession, RemoteScreen from screenData: ' +
                    JSON.stringify(u) +
                    ' is not online.'
                )
              ),
              Y.gO());
        },
        5
      );
    },
    Ozy = function (Y, u) {
      g.iL(Y.KG);
      Y.KG = 0;
      u
        ? Y.config_.enableCastLoungeToken && u.loungeToken
          ? u.deviceId
            ? (Y.K && Y.K.uuid == u.deviceId) ||
              (u.loungeTokenRefreshIntervalMs
                ? up$(
                    Y,
                    {
                      name: Y.j.friendlyName,
                      screenId: u.screenId,
                      loungeToken: u.loungeToken,
                      dialId: u.deviceId,
                      screenIdType: 'shortLived',
                    },
                    u.loungeTokenRefreshIntervalMs
                  )
                : (g.VM(
                    Error(
                      'No loungeTokenRefreshIntervalMs presents in mdxSessionStatusData: ' +
                        JSON.stringify(u) +
                        '.'
                    )
                  ),
                  $3Q(Y, u.screenId)))
            : (g.VM(
                Error('No device id presents in mdxSessionStatusData: ' + JSON.stringify(u) + '.')
              ),
              $3Q(Y, u.screenId))
          : $3Q(Y, u.screenId)
        : Y.gO(Error('Waiting for session status timed out.'));
    },
    aXL = function (Y, u) {
      g.iL(Y.J);
      Y.J = 0;
      var n = null;
      if (u)
        if (u.loungeToken) {
          var U;
          ((U = Y.K) == null ? void 0 : U.token) == u.loungeToken && (n = 'staleLoungeToken');
        } else n = 'missingLoungeToken';
      else n = 'noLoungeTokenResponse';
      n
        ? (Y.info(
            'Did not receive a new lounge token in onLoungeToken_ with data: ' +
              (JSON.stringify(u) + ', error: ' + n)
          ),
          (Y.N = n),
          JDB(Y, 3e4))
        : (VvR(Y, u.loungeToken),
          (Y.jG = !1),
          (Y.N = 'unknown'),
          JDB(Y, u.loungeTokenRefreshIntervalMs));
    },
    YLC = function (Y, u, n, U) {
      g.iL(Y.W);
      Y.W = 0;
      gHR(Y.G, u, function (k) {
        k || U < 0
          ? n(k)
          : (Y.W = g.QS(function () {
              YLC(Y, u, n, U - 1);
            }, 300));
      });
    },
    nk$ = function (Y) {
      g.iL(Y.Z);
      Y.Z = 0;
      g.iL(Y.W);
      Y.W = 0;
      g.iL(Y.KG);
      Y.KG = 0;
      g.iL(Y.J);
      Y.J = 0;
      g.iL(Y.S);
      Y.S = 0;
    },
    sI = function (Y, u, n, U) {
      ZQ.call(this, Y, u, 'DialSession');
      this.config_ = U;
      this.X = this.Z = null;
      this.DW = '';
      this.JJ = n;
      this.Fk = null;
      this.KG = function () {};
      this.N = NaN;
      this.MF = (0, g.fR)(this.ij, this);
      this.J = function () {};
      this.S = this.W = 0;
      this.oV = !1;
      this.jG = 'unknown';
    },
    d1 = function (Y) {
      var u;
      return !!(Y.config_.enableDialLoungeToken && ((u = Y.X) == null ? 0 : u.getDialAppInfo));
    },
    U9g = function (Y) {
      Y.J = Y.G.dQ(
        Y.DW,
        Y.j.label,
        Y.j.friendlyName,
        d1(Y),
        function (u, n) {
          Y.J = function () {};
          Y.oV = !0;
          TM(Y, u);
          u.idType == 'shortLived' && n > 0 && GM(Y, n);
        },
        function (u) {
          Y.J = function () {};
          Y.gO(u);
        }
      );
    },
    kSC = function (Y) {
      var u = {};
      u.pairingCode = Y.DW;
      u.theme = Y.JJ;
      kP$() && (u.env_useStageMdx = 1);
      return g.r3(u);
    },
    m9Q = function (Y) {
      return new Promise(function (u) {
        Y.DW = HvJ();
        if (Y.Fk) {
          var n = new chrome.cast.DialLaunchResponse(!0, kSC(Y));
          u(n);
          U9g(Y);
        } else
          ((Y.KG = function () {
            g.iL(Y.N);
            Y.KG = function () {};
            Y.N = NaN;
            var U = new chrome.cast.DialLaunchResponse(!0, kSC(Y));
            u(U);
            U9g(Y);
          }),
            (Y.N = g.QS(function () {
              Y.KG();
            }, 100)));
      });
    },
    PaQ = function (Y, u, n) {
      Y.info('initOnConnectedScreenDataPromise_: Received screenData: ' + JSON.stringify(u));
      var U = new C8(u);
      return new Promise(function (k) {
        Xhg(
          Y,
          U,
          function (m) {
            m
              ? ((Y.oV = !0), ii(Y.G, U), TM(Y, U), GM(Y, n))
              : g.VM(
                  Error(
                    'DialSession, RemoteScreen from screenData: ' +
                      JSON.stringify(u) +
                      ' is not online.'
                  )
                );
            k(m);
          },
          5
        );
      }).then(function (k) {
        return k ? new chrome.cast.DialLaunchResponse(!1) : m9Q(Y);
      });
    },
    SLC = function (Y, u) {
      var n = Y.Z.receiver.label,
        U = Y.j.friendlyName;
      return new Promise(function (k) {
        IXJ(
          Y.G,
          n,
          u,
          U,
          function (m) {
            m && m.token && TM(Y, m);
            k(m);
          },
          function (m) {
            r1(Y, 'Failed to get DIAL screen: ' + m);
            k(null);
          }
        );
      }).then(function (k) {
        return k && k.token ? new chrome.cast.DialLaunchResponse(!1) : m9Q(Y);
      });
    },
    Xhg = function (Y, u, n, U) {
      g.iL(Y.W);
      Y.W = 0;
      gHR(Y.G, u, function (k) {
        k || U < 0
          ? n(k)
          : (Y.W = g.QS(function () {
              Xhg(Y, u, n, U - 1);
            }, 300));
      });
    },
    GM = function (Y, u) {
      Y.info('getDialAppInfoWithTimeout_ ' + u);
      d1(Y) &&
        (g.iL(Y.S),
        (Y.S = 0),
        u == 0
          ? CaB(Y)
          : (Y.S = g.QS(function () {
              CaB(Y);
            }, u)));
    },
    CaB = function (Y) {
      d1(Y) &&
        Y.X.getDialAppInfo(
          function (u) {
            Y.info('getDialAppInfo dialLaunchData: ' + JSON.stringify(u));
            u = u.extraData || {};
            var n = null;
            if (u.loungeToken) {
              var U;
              ((U = Y.K) == null ? void 0 : U.token) == u.loungeToken && (n = 'staleLoungeToken');
            } else n = 'missingLoungeToken';
            n
              ? ((Y.jG = n), GM(Y, 3e4))
              : ((Y.oV = !1),
                (Y.jG = 'unknown'),
                VvR(Y, u.loungeToken),
                GM(Y, u.loungeTokenRefreshIntervalMs));
          },
          function (u) {
            Y.info('getDialAppInfo error: ' + u);
            Y.jG = 'noLoungeTokenResponse';
            GM(Y, 3e4);
          }
        );
    },
    f8L = function (Y) {
      g.iL(Y.W);
      Y.W = 0;
      g.iL(Y.S);
      Y.S = 0;
      Y.J();
      Y.J = function () {};
      g.iL(Y.N);
    },
    AV = function (Y, u) {
      ZQ.call(this, Y, u, 'ManualSession');
      this.X = g.QS((0, g.fR)(this.hg, this, null), 150);
    },
    jQ = function (Y, u) {
      g.ud.call(this);
      this.config_ = u;
      this.j = Y;
      this.Z = u.appId || '233637DE';
      this.G = u.theme || 'cl';
      this.N = u.disableCastApi || !1;
      this.W = u.forceMirroring || !1;
      this.K = null;
      this.S = !1;
      this.X = [];
      this.J = (0, g.fR)(this.MuV, this);
    },
    QB$ = function (Y, u) {
      return u
        ? g.G$(
            Y.X,
            function (n) {
              return f8(u, n.label);
            },
            Y
          )
        : null;
    },
    Ke = function (Y) {
      ne('Controller', Y);
    },
    GlR = function (Y) {
      window.chrome && chrome.cast && chrome.cast.logMessage && chrome.cast.logMessage(Y);
    },
    pe = function (Y) {
      return Y.S || !!Y.X.length || !!Y.K;
    },
    Le = function (Y, u, n) {
      u != Y.K &&
        (g.nc(Y.K),
        (Y.K = u)
          ? (n
              ? Y.publish('yt-remote-cast2-receiver-resumed', u.j)
              : Y.publish('yt-remote-cast2-receiver-selected', u.j),
            u.subscribe('sessionScreen', (0, g.fR)(Y.ea, Y, u)),
            u.subscribe('sessionFailed', function () {
              return NlG(Y, u);
            }),
            u.K ? Y.publish('yt-remote-cast2-session-change', u.K) : n && Y.K.hg(null))
          : Y.publish('yt-remote-cast2-session-change', null));
    },
    NlG = function (Y, u) {
      Y.K == u && Y.publish('yt-remote-cast2-session-failed');
    },
    iAq = function (Y) {
      var u = Y.j.EB(),
        n = Y.K && Y.K.j;
      Y = g.dA(
        u,
        function (U) {
          n && f8(U, n.label) && (n = null);
          var k = U.uuid ? U.uuid : U.id,
            m = QB$(this, U);
          m
            ? ((m.label = k), (m.friendlyName = U.name))
            : ((m = new chrome.cast.Receiver(k, U.name)),
              (m.receiverType = chrome.cast.ReceiverType.CUSTOM));
          return m;
        },
        Y
      );
      n &&
        (n.receiverType != chrome.cast.ReceiverType.CUSTOM &&
          ((n = new chrome.cast.Receiver(n.label, n.friendlyName)),
          (n.receiverType = chrome.cast.ReceiverType.CUSTOM)),
        Y.push(n));
      return Y;
    },
    A2$ = function (Y, u, n, U) {
      U.disableCastApi
        ? tV('Cannot initialize because disabled by Mdx config.')
        : ZAG()
          ? Tly(u, U) &&
            (r2Q(!0),
            window.chrome && chrome.cast && chrome.cast.isAvailable
              ? M6B(Y, n)
              : ((window.__onGCastApiAvailable = function (k, m) {
                  k
                    ? M6B(Y, n)
                    : (Bs('Failed to load cast API: ' + m),
                      sBQ(!1),
                      r2Q(!1),
                      g.vk('yt-remote-cast-available'),
                      g.vk('yt-remote-cast-receiver'),
                      d9R(),
                      n(!1));
                }),
                U.loadCastApiSetupScript
                  ? g.kk(GSq)
                  : window.navigator.userAgent.indexOf('Android') >= 0 &&
                      window.navigator.userAgent.indexOf('Chrome/') >= 0 &&
                      window.navigator.presentation
                    ? Xk$() >= 60 && TT$()
                    : !window.chrome ||
                        !window.navigator.presentation ||
                        window.navigator.userAgent.indexOf('Edge') >= 0
                      ? fmQ()
                      : Xk$() >= 89
                        ? MoX()
                        : (ZbG(), d_(r6q.map(QUu)))))
          : tV('Cannot initialize because not running Chrome');
    },
    d9R = function () {
      tV('dispose');
      var Y = og();
      Y && Y.dispose();
      g.Y$('yt.mdx.remote.cloudview.instance_', null);
      jBy(!1);
      g.a9(Kky);
      Kky.length = 0;
    },
    cs = function () {
      return !!g.ck('yt-remote-cast-installed');
    },
    phR = function () {
      var Y = g.ck('yt-remote-cast-receiver');
      return Y ? Y.friendlyName : null;
    },
    LkL = function () {
      tV('clearCurrentReceiver');
      g.vk('yt-remote-cast-receiver');
    },
    t6L = function () {
      return cs()
        ? og()
          ? og().getCastSession()
          : (Bs('getCastSelector: Cast is not initialized.'), null)
        : (Bs('getCastSelector: Cast API is not installed!'), null);
    },
    BlJ = function () {
      cs()
        ? og()
          ? vs()
            ? (tV('Requesting cast selector.'), og().requestSession())
            : (tV('Wait for cast API to be ready to request the session.'),
              Kky.push(g.q3('yt-remote-cast2-api-ready', BlJ)))
          : Bs('requestCastSelector: Cast is not initialized.')
        : Bs('requestCastSelector: Cast API is not installed!');
    },
    Rg = function (Y, u) {
      vs()
        ? og().setConnectedScreenStatus(Y, u)
        : Bs('setConnectedScreenStatus called before ready.');
    },
    ZAG = function () {
      var Y = g.Wq().search(/ (CrMo|Chrome|CriOS)\//) >= 0;
      return g.sP || Y;
    },
    ok$ = function (Y, u) {
      og().init(Y, u);
    },
    Tly = function (Y, u) {
      var n = !1;
      og() ||
        ((Y = new jQ(Y, u)),
        Y.subscribe('yt-remote-cast2-availability-change', function (U) {
          g.oU('yt-remote-cast-available', U);
          MC('yt-remote-cast2-availability-change', U);
        }),
        Y.subscribe('yt-remote-cast2-receiver-selected', function (U) {
          tV('onReceiverSelected: ' + U.friendlyName);
          g.oU('yt-remote-cast-receiver', U);
          MC('yt-remote-cast2-receiver-selected', U);
        }),
        Y.subscribe('yt-remote-cast2-receiver-resumed', function (U) {
          tV('onReceiverResumed: ' + U.friendlyName);
          g.oU('yt-remote-cast-receiver', U);
          MC('yt-remote-cast2-receiver-resumed', U);
        }),
        Y.subscribe('yt-remote-cast2-session-change', function (U) {
          tV('onSessionChange: ' + Qo(U));
          U || g.vk('yt-remote-cast-receiver');
          MC('yt-remote-cast2-session-change', U);
        }),
        g.Y$('yt.mdx.remote.cloudview.instance_', Y),
        (n = !0));
      tV('cloudview.createSingleton_: ' + n);
      return n;
    },
    og = function () {
      return g.nR('yt.mdx.remote.cloudview.instance_');
    },
    M6B = function (Y, u) {
      sBQ(!0);
      r2Q(!1);
      ok$(Y, function (n) {
        n
          ? (jBy(!0), g.$H('yt-remote-cast2-api-ready'))
          : (Bs('Failed to initialize cast API.'),
            sBQ(!1),
            g.vk('yt-remote-cast-available'),
            g.vk('yt-remote-cast-receiver'),
            d9R());
        u(n);
      });
    },
    tV = function (Y) {
      ne('cloudview', Y);
    },
    Bs = function (Y) {
      ne('cloudview', Y);
    },
    sBQ = function (Y) {
      tV('setCastInstalled_ ' + Y);
      g.oU('yt-remote-cast-installed', Y);
    },
    vs = function () {
      return !!g.nR('yt.mdx.remote.cloudview.apiReady_');
    },
    jBy = function (Y) {
      tV('setApiReady_ ' + Y);
      g.Y$('yt.mdx.remote.cloudview.apiReady_', Y);
    },
    r2Q = function (Y) {
      g.Y$('yt.mdx.remote.cloudview.initializing_', Y);
    },
    DQ = function (Y) {
      this.index = -1;
      this.videoId = this.listId = '';
      this.volume = this.playerState = -1;
      this.muted = !1;
      this.audioTrackId = null;
      this.J = this.W = 0;
      this.trackData = null;
      this.ul = this.ZC = !1;
      this.Z = this.X = this.S = this.j = 0;
      this.K = NaN;
      this.G = !1;
      this.reset(Y);
    },
    c2B = function (Y) {
      Y.audioTrackId = null;
      Y.trackData = null;
      Y.playerState = -1;
      Y.ZC = !1;
      Y.ul = !1;
      Y.W = 0;
      Y.J = g.iQ();
      Y.j = 0;
      Y.S = 0;
      Y.X = 0;
      Y.Z = 0;
      Y.K = NaN;
      Y.G = !1;
    },
    xt = function (Y) {
      return Y.isPlaying() ? (g.iQ() - Y.J) / 1e3 : 0;
    },
    li = function (Y, u) {
      Y.W = u;
      Y.J = g.iQ();
    },
    hV = function (Y) {
      switch (Y.playerState) {
        case 1:
        case 1081:
          return (g.iQ() - Y.J) / 1e3 + Y.W;
        case -1e3:
          return 0;
      }
      return Y.W;
    },
    vkq = function (Y) {
      return Y.G ? Y.S + xt(Y) : Y.S;
    },
    w1 = function (Y, u, n) {
      var U = Y.videoId;
      Y.videoId = u;
      Y.index = n;
      u != U && c2B(Y);
    },
    RTG = function (Y) {
      var u = {};
      u.index = Y.index;
      u.listId = Y.listId;
      u.videoId = Y.videoId;
      u.playerState = Y.playerState;
      u.volume = Y.volume;
      u.muted = Y.muted;
      u.audioTrackId = Y.audioTrackId;
      u.trackData = g.Ml(Y.trackData);
      u.hasPrevious = Y.ZC;
      u.hasNext = Y.ul;
      u.playerTime = Y.W;
      u.playerTimeAt = Y.J;
      u.seekableStart = Y.j;
      u.seekableEnd = Y.S;
      u.duration = Y.X;
      u.loadedTime = Y.Z;
      u.liveIngestionTime = Y.K;
      return u;
    },
    eQ = function (Y, u) {
      g.ud.call(this);
      var n = this;
      this.X = 0;
      this.G = Y;
      this.W = [];
      this.J = new q$$();
      this.j = this.K = null;
      this.N = (0, g.fR)(this.wzg, this);
      this.S = (0, g.fR)(this.Mj, this);
      this.Z = (0, g.fR)(this.cJz, this);
      this.KG = (0, g.fR)(this.z22, this);
      var U = 0;
      Y
        ? ((U = Y.getProxyState()),
          U != 3 && (Y.subscribe('proxyStateChange', this.ge, this), D9q(this)))
        : (U = 3);
      U != 0 &&
        (u
          ? this.ge(U)
          : g.QS(function () {
              n.ge(U);
            }, 0));
      (Y = t6L()) && Ws(this, Y);
      this.subscribe('yt-remote-cast2-session-change', this.KG);
    },
    bi = function (Y) {
      return new DQ(Y.G.getPlayerContextData());
    },
    D9q = function (Y) {
      g.Jy(
        'nowAutoplaying autoplayDismissed remotePlayerChange remoteQueueChange autoplayModeChange autoplayUpNext previousNextChange multiStateLoopEnabled loopModeChange'.split(
          ' '
        ),
        function (u) {
          this.W.push(this.G.subscribe(u, g.QC(this.Wok, u), this));
        },
        Y
      );
    },
    x9C = function (Y) {
      g.Jy(
        Y.W,
        function (u) {
          this.G.unsubscribeByKey(u);
        },
        Y
      );
      Y.W.length = 0;
    },
    Ig = function (Y) {
      return Y.getState() == 1;
    },
    zM = function (Y, u) {
      var n = Y.J;
      n.K.length + n.j.length < 50 && Y.J.enqueue(u);
    },
    l8R = function (Y, u, n) {
      var U = bi(Y);
      li(U, n);
      U.playerState != -1e3 && (U.playerState = u);
      g1(Y, U);
    },
    EI = function (Y, u, n) {
      Y.G.sendMessage(u, n);
    },
    g1 = function (Y, u) {
      x9C(Y);
      Y.G.setPlayerContextData(RTG(u));
      D9q(Y);
    },
    Ws = function (Y, u) {
      Y.j && (Y.j.removeUpdateListener(Y.N), Y.j.removeMediaListener(Y.S), Y.Mj(null));
      Y.j = u;
      Y.j &&
        (UI('Setting cast session: ' + Y.j.sessionId),
        Y.j.addUpdateListener(Y.N),
        Y.j.addMediaListener(Y.S),
        Y.j.media.length && Y.Mj(Y.j.media[0]));
    },
    hTg = function (Y) {
      var u = Y.K.media,
        n = Y.K.customData;
      if (u && n) {
        var U = bi(Y);
        u.contentId != U.videoId && UI('Cast changing video to: ' + u.contentId);
        U.videoId = u.contentId;
        U.playerState = n.playerState;
        li(U, Y.K.getEstimatedTime());
        g1(Y, U);
      } else UI('No cast media video. Ignoring state update.');
    },
    Hs = function (Y, u, n) {
      return (0, g.fR)(function (U) {
        this.nk('Failed to ' + u + ' with cast v2 channel. Error code: ' + U.code);
        U.code != chrome.cast.ErrorCode.TIMEOUT &&
          (this.nk('Retrying ' + u + ' using MDx browser channel.'), EI(this, u, n));
      }, Y);
    },
    OI = function (Y, u, n, U) {
      U = U === void 0 ? !1 : U;
      g.ud.call(this);
      var k = this;
      this.W = NaN;
      this.DW = !1;
      this.N = this.Z = this.oV = this.jG = NaN;
      this.KG = [];
      this.J = this.S = this.G = this.K = this.j = null;
      this.Fk = Y;
      this.MF = U;
      this.KG.push(
        g.s2(window, 'beforeunload', function () {
          k.Rs(2);
        })
      );
      this.X = [];
      this.K = new DQ();
      this.JJ = u.id;
      this.rg = u.idType;
      this.j = d3C(this.Fk, n, this.zv, this.rg == 'shortLived', this.JJ);
      this.j.listen('channelOpened', function () {
        whB(k);
      });
      this.j.listen('channelClosed', function () {
        y5('Channel closed');
        isNaN(k.W) ? Tx(!0) : Tx();
        k.dispose();
      });
      this.j.listen('channelError', function (m) {
        Tx();
        isNaN(k.GA())
          ? (m == 1 && k.rg == 'shortLived' && k.publish('browserChannelAuthError', m),
            y5('Channel error: ' + m + ' without reconnection'),
            k.dispose())
          : ((k.DW = !0),
            y5('Channel error: ' + m + ' with reconnection in ' + k.GA() + ' ms'),
            V5(k, 2));
      });
      this.j.listen('channelMessage', function (m) {
        WkR(k, m);
      });
      this.j.KL(u.token);
      this.subscribe('remoteQueueChange', function () {
        var m = k.K.videoId;
        g.RU() && g.oU('yt-remote-session-video-id', m);
      });
    },
    eTG = function (Y) {
      return g.G$(Y.X, function (u) {
        return u.type == 'LOUNGE_SCREEN';
      });
    },
    y5 = function (Y) {
      ne('conn', Y);
    },
    V5 = function (Y, u) {
      Y.publish('proxyStateChange', u);
    },
    bAL = function (Y) {
      Y.W = g.QS(function () {
        y5('Connecting timeout');
        Y.Rs(1);
      }, 2e4);
    },
    I8C = function (Y) {
      g.iL(Y.W);
      Y.W = NaN;
    },
    zTC = function (Y) {
      g.iL(Y.jG);
      Y.jG = NaN;
    },
    EkR = function (Y) {
      gkX(Y);
      Y.oV = g.QS(function () {
        Fm(Y, 'getNowPlaying');
      }, 2e4);
    },
    gkX = function (Y) {
      g.iL(Y.oV);
      Y.oV = NaN;
    },
    whB = function (Y) {
      y5('Channel opened');
      Y.DW &&
        ((Y.DW = !1),
        zTC(Y),
        (Y.jG = g.QS(function () {
          y5('Timing out waiting for a screen.');
          Y.Rs(1);
        }, 15e3)));
    },
    y2$ = function (Y, u) {
      var n = null;
      if (u) {
        var U = eTG(Y);
        U &&
          (n = {
            clientName: U.clientName,
            deviceMake: U.brand,
            deviceModel: U.model,
            osVersion: U.osVersion,
          });
      }
      g.Y$('yt.mdx.remote.remoteClient_', n);
      u && (I8C(Y), zTC(Y));
      n = Y.j.OZ() && isNaN(Y.W);
      u == n
        ? u && (V5(Y, 1), Fm(Y, 'getSubtitlesTrack'))
        : u
          ? (Y.f9() && Y.K.reset(), V5(Y, 1), Fm(Y, 'getNowPlaying'), HAR(Y))
          : Y.Rs(1);
    },
    V6$ = function (Y, u) {
      var n = u.params.videoId;
      delete u.params.videoId;
      n == Y.K.videoId &&
        (g.i4(u.params) ? (Y.K.trackData = null) : (Y.K.trackData = u.params),
        Y.publish('remotePlayerChange'));
    },
    OAC = function (Y, u, n) {
      var U = u.params.videoId || u.params.video_id,
        k = parseInt(u.params.currentIndex, 10);
      Y.K.listId = u.params.listId || Y.K.listId;
      w1(Y.K, U, k);
      Y.publish('remoteQueueChange', n);
    },
    J2q = function (Y, u) {
      u.params = u.params || {};
      OAC(Y, u, 'NOW_PLAYING_MAY_CHANGE');
      FkC(Y, u);
      Y.publish('autoplayDismissed');
    },
    FkC = function (Y, u) {
      var n = parseInt(u.params.currentTime || u.params.current_time, 10);
      li(Y.K, isNaN(n) ? 0 : n);
      n = parseInt(u.params.state, 10);
      n = isNaN(n) ? -1 : n;
      n == -1 && Y.K.playerState == -1e3 && (n = -1e3);
      Y.K.playerState = n;
      n = Number(u.params.loadedTime);
      Y.K.Z = isNaN(n) ? 0 : n;
      Y.K.Jp(Number(u.params.duration));
      n = Y.K;
      var U = Number(u.params.liveIngestionTime);
      n.K = U;
      n.G = isNaN(U) ? !1 : !0;
      n = Y.K;
      U = Number(u.params.seekableStartTime);
      u = Number(u.params.seekableEndTime);
      n.j = isNaN(U) ? 0 : U;
      n.S = isNaN(u) ? 0 : u;
      Y.K.playerState == 1 ? EkR(Y) : gkX(Y);
      Y.publish('remotePlayerChange');
    },
    qLq = function (Y, u) {
      if (Y.K.playerState != -1e3) {
        var n = 1085;
        switch (parseInt(u.params.adState, 10)) {
          case 1:
            n = 1081;
            break;
          case 2:
            n = 1084;
            break;
          case 0:
            n = 1083;
        }
        Y.K.playerState = n;
        u = parseInt(u.params.currentTime, 10);
        li(Y.K, isNaN(u) ? 0 : u);
        Y.publish('remotePlayerChange');
      }
    },
    a8$ = function (Y, u) {
      var n = u.params.muted == 'true';
      Y.K.volume = parseInt(u.params.volume, 10);
      Y.K.muted = n;
      Y.publish('remotePlayerChange');
    },
    $9C = function (Y, u) {
      Y.S = u.params.videoId;
      Y.publish('nowAutoplaying', parseInt(u.params.timeout, 10));
    },
    YCq = function (Y, u) {
      Y.S = u.params.videoId || null;
      Y.publish('autoplayUpNext', Y.S);
    },
    uou = function (Y, u) {
      Y.J = u.params.autoplayMode;
      Y.publish('autoplayModeChange', Y.J);
      Y.J == 'DISABLED' && Y.publish('autoplayDismissed');
    },
    nCq = function (Y, u) {
      var n = u.params.hasNext == 'true';
      Y.K.ZC = u.params.hasPrevious == 'true';
      Y.K.ul = n;
      Y.publish('previousNextChange');
    },
    WkR = function (Y, u) {
      u = u.message;
      u.params
        ? y5('Received: action=' + u.action + ', params=' + g.zE(u.params))
        : y5('Received: action=' + u.action + ' {}');
      switch (u.action) {
        case 'loungeStatus':
          u = U1(u.params.devices);
          Y.X = g.dA(u, function (U) {
            return new SY(U);
          });
          u = !!g.G$(Y.X, function (U) {
            return U.type == 'LOUNGE_SCREEN';
          });
          y2$(Y, u);
          u = Y.N9('mlm');
          Y.publish('multiStateLoopEnabled', u);
          break;
        case 'loungeScreenDisconnected':
          g.cu(Y.X, function (U) {
            return U.type == 'LOUNGE_SCREEN';
          });
          y2$(Y, !1);
          break;
        case 'remoteConnected':
          var n = new SY(U1(u.params.device));
          g.G$(Y.X, function (U) {
            return U.equals(n);
          }) || UIu(Y.X, n);
          break;
        case 'remoteDisconnected':
          n = new SY(U1(u.params.device));
          g.cu(Y.X, function (U) {
            return U.equals(n);
          });
          break;
        case 'gracefulDisconnect':
          break;
        case 'playlistModified':
          OAC(Y, u, 'QUEUE_MODIFIED');
          break;
        case 'nowPlaying':
          J2q(Y, u);
          break;
        case 'onStateChange':
          FkC(Y, u);
          break;
        case 'onAdStateChange':
          qLq(Y, u);
          break;
        case 'onVolumeChanged':
          a8$(Y, u);
          break;
        case 'onSubtitlesTrackChanged':
          V6$(Y, u);
          break;
        case 'nowAutoplaying':
          $9C(Y, u);
          break;
        case 'autoplayDismissed':
          Y.publish('autoplayDismissed');
          break;
        case 'autoplayUpNext':
          YCq(Y, u);
          break;
        case 'onAutoplayModeChanged':
          uou(Y, u);
          break;
        case 'onHasPreviousNextChanged':
          nCq(Y, u);
          break;
        case 'requestAssistedSignIn':
          Y.publish('assistedSignInRequested', u.params.authCode);
          break;
        case 'onLoopModeChanged':
          Y.publish('loopModeChange', u.params.loopMode);
          break;
        default:
          y5('Unrecognized action: ' + u.action);
      }
    },
    HAR = function (Y) {
      g.iL(Y.N);
      Y.N = g.QS(function () {
        Y.Rs(1);
      }, 864e5);
    },
    Fm = function (Y, u, n) {
      n ? y5('Sending: action=' + u + ', params=' + g.zE(n)) : y5('Sending: action=' + u);
      Y.j.sendMessage(u, n);
    },
    UnG = function (Y) {
      Ps.call(this, 'ScreenServiceProxy');
      this.o_ = Y;
      this.K = [];
      this.K.push(this.o_.$_s('screenChange', (0, g.fR)(this.ZS, this)));
      this.K.push(this.o_.$_s('onlineScreenChange', (0, g.fR)(this.lFF, this)));
    },
    SCB = function (Y, u) {
      UxC();
      if (!r_ || !r_.get('yt-remote-disable-remote-module-for-dev')) {
        u = g.z6('MDX_CONFIG') || u;
        OvC();
        azL();
        JV || ((JV = new $2(u ? u.loungeApiHost : void 0)), kP$() && (JV.K = '/api/loungedev'));
        qh ||
          ((qh = g.nR('yt.mdx.remote.deferredProxies_') || []),
          g.Y$('yt.mdx.remote.deferredProxies_', qh));
        kn$();
        var n = ag();
        if (!n) {
          var U = new Nh(JV, u ? u.disableAutomaticScreenCache || !1 : !1);
          g.Y$('yt.mdx.remote.screenService_', U);
          n = ag();
          var k = {};
          u &&
            (k = {
              appId: u.appId,
              disableDial: u.disableDial,
              theme: u.theme,
              loadCastApiSetupScript: u.loadCastApiSetupScript,
              disableCastApi: u.disableCastApi,
              enableDialLoungeToken: u.enableDialLoungeToken,
              enableCastLoungeToken: u.enableCastLoungeToken,
              forceMirroring: u.forceMirroring,
            });
          g.Y$(
            'yt.mdx.remote.enableConnectWithInitialState_',
            u ? u.enableConnectWithInitialState || !1 : !1
          );
          A2$(
            Y,
            U,
            function (m) {
              m
                ? $t() && Rg($t(), 'YouTube TV')
                : U.subscribe('onlineScreenChange', function () {
                    MC('yt-remote-receiver-availability-change');
                  });
            },
            k
          );
        }
        u &&
          !g.nR('yt.mdx.remote.initialized_') &&
          (g.Y$('yt.mdx.remote.initialized_', !0),
          YZ('Initializing: ' + g.zE(u)),
          up.push(
            g.q3('yt-remote-cast2-api-ready', function () {
              MC('yt-remote-api-ready');
            })
          ),
          up.push(
            g.q3('yt-remote-cast2-availability-change', function () {
              MC('yt-remote-receiver-availability-change');
            })
          ),
          up.push(
            g.q3('yt-remote-cast2-receiver-selected', function () {
              nf(null);
              MC('yt-remote-auto-connect', 'cast-selector-receiver');
            })
          ),
          up.push(
            g.q3('yt-remote-cast2-receiver-resumed', function () {
              MC('yt-remote-receiver-resumed', 'cast-selector-receiver');
            })
          ),
          up.push(g.q3('yt-remote-cast2-session-change', mnG)),
          up.push(
            g.q3('yt-remote-connection-change', function (m) {
              m ? Rg($t(), 'YouTube TV') : UO() || (Rg(null, null), LkL());
            })
          ),
          up.push(
            g.q3('yt-remote-cast2-session-failed', function () {
              MC('yt-remote-connection-failed');
            })
          ),
          (Y = XrL()),
          u.isAuto && (Y.id += '#dial'),
          (k = u.capabilities || []),
          k.length > 0 && (Y.capabilities = k),
          (Y.name = u.device),
          (Y.app = u.app),
          (u = u.theme) && (Y.theme = u),
          YZ(' -- with channel params: ' + g.zE(Y)),
          Y
            ? (g.oU('yt-remote-session-app', Y.app), g.oU('yt-remote-session-name', Y.name))
            : (g.vk('yt-remote-session-app'), g.vk('yt-remote-session-name')),
          g.Y$('yt.mdx.remote.channelParams_', Y),
          n.start(),
          $t() || P2R());
      }
    },
    C2J = function () {
      var Y = ag().o_.$_gos();
      var u = kZ();
      u && mE() && (VsL(Y, u) || Y.push(u));
      return yk$(Y);
    },
    Qbq = function () {
      var Y = fIR();
      !Y && cs() && phR() && (Y = { key: 'cast-selector-receiver', name: phR() });
      return Y;
    },
    fIR = function () {
      var Y = C2J(),
        u = kZ();
      u || (u = UO());
      return g.G$(Y, function (n) {
        return u && f8(u, n.key) ? !0 : !1;
      });
    },
    kZ = function () {
      var Y = $t();
      if (!Y) return null;
      var u = ag().XS();
      return NC(u, Y);
    },
    mnG = function (Y) {
      YZ('remote.onCastSessionChange_: ' + Qo(Y));
      if (Y) {
        var u = kZ();
        if (u && u.id == Y.id) {
          if ((Rg(u.id, 'YouTube TV'), Y.idType == 'shortLived' && (Y = Y.token)))
            (Xv && (Xv.token = Y), (u = mE()) && u.KL(Y));
        } else (u && PE(), S5(Y, 1));
      } else mE() && PE();
    },
    PE = function () {
      vs() ? og().stopSession() : Bs('stopSession called before API ready.');
      var Y = mE();
      Y && (Y.disconnect(1), NUB(null));
    },
    iC$ = function () {
      var Y = mE();
      return !!Y && Y.getProxyState() != 3;
    },
    YZ = function (Y) {
      ne('remote', Y);
    },
    ag = function () {
      if (!ZCq) {
        var Y = g.nR('yt.mdx.remote.screenService_');
        ZCq = Y ? new UnG(Y) : null;
      }
      return ZCq;
    },
    $t = function () {
      return g.nR('yt.mdx.remote.currentScreenId_');
    },
    TUB = function (Y) {
      g.Y$('yt.mdx.remote.currentScreenId_', Y);
    },
    rl$ = function () {
      return g.nR('yt.mdx.remote.connectData_');
    },
    nf = function (Y) {
      g.Y$('yt.mdx.remote.connectData_', Y);
    },
    mE = function () {
      return g.nR('yt.mdx.remote.connection_');
    },
    NUB = function (Y) {
      var u = mE();
      nf(null);
      Y || TUB('');
      g.Y$('yt.mdx.remote.connection_', Y);
      qh &&
        (g.Jy(qh, function (n) {
          n(Y);
        }),
        (qh.length = 0));
      u && !Y
        ? MC('yt-remote-connection-change', !1)
        : !u && Y && MC('yt-remote-connection-change', !0);
    },
    UO = function () {
      var Y = g.RU();
      if (!Y) return null;
      var u = ag();
      if (!u) return null;
      u = u.XS();
      return NC(u, Y);
    },
    S5 = function (Y, u) {
      $t();
      kZ() && kZ();
      if (Cf) Xv = Y;
      else {
        TUB(Y.id);
        var n = g.nR('yt.mdx.remote.enableConnectWithInitialState_') || !1;
        Y = new OI(JV, Y, XrL(), n);
        Y.connect(u, rl$());
        Y.subscribe('beforeDisconnect', function (U) {
          MC('yt-remote-before-disconnect', U);
        });
        Y.subscribe('beforeDispose', function () {
          mE() && (mE(), NUB(null));
        });
        Y.subscribe('browserChannelAuthError', function () {
          var U = kZ();
          U &&
            U.idType == 'shortLived' &&
            (vs()
              ? og().handleBrowserChannelAuthError()
              : Bs('refreshLoungeToken called before API ready.'));
        });
        NUB(Y);
      }
    },
    P2R = function () {
      var Y = UO();
      Y
        ? (YZ('Resume connection to: ' + Qo(Y)), S5(Y, 0))
        : (Tx(), LkL(), YZ('Skipping connecting because no session screen found.'));
    },
    kn$ = function () {
      var Y = XrL();
      if (g.i4(Y)) {
        Y = Zl();
        var u = g.ck('yt-remote-session-name') || '',
          n = g.ck('yt-remote-session-app') || '';
        Y = { device: 'REMOTE_CONTROL', id: Y, name: u, app: n, mdxVersion: 3 };
        Y.authuser = String(g.z6('SESSION_INDEX', '0'));
        (u = g.z6('DELEGATED_SESSION_ID')) && (Y.pageId = String(u));
        g.Y$('yt.mdx.remote.channelParams_', Y);
      }
    },
    XrL = function () {
      return g.nR('yt.mdx.remote.channelParams_') || {};
    },
    dng = function (Y, u, n) {
      g.e.call(this);
      var U = this;
      this.K = Y;
      this.L = u;
      this.YV = n;
      this.events = new g.j3(this);
      this.J = !1;
      this.W = new g.RZ(64);
      this.j = new g.Vp(this.HT, 500, this);
      this.X = new g.Vp(this.AB, 1e3, this);
      this.Z = new Gx(this.maG, 0, this);
      this.G = {};
      this.N = new g.Vp(this.lz, 1e3, this);
      this.S = new g.qs(this.seekTo, 1e3, this);
      this.KG = this.events.B(this.L, 'onVolumeChange', function (k) {
        MgX(U, k);
      });
      g.b(this, this.events);
      this.events.B(u, 'onCaptionsTrackListChanged', this.y_g);
      this.events.B(u, 'captionschanged', this.EwZ);
      this.events.B(u, 'captionssettingschanged', this.dN);
      this.events.B(u, 'videoplayerreset', this.pg);
      this.events.B(u, 'mdxautoplaycancel', function () {
        U.YV.O4();
      });
      u.V('enable_mdx_video_play_directly') &&
        this.events.B(u, 'videodatachange', function () {
          sb$(U.K) || ff(U) || QG(U, 0);
        });
      Y = this.YV;
      Y.gg();
      Y.subscribe('proxyStateChange', this.k0, this);
      Y.subscribe('remotePlayerChange', this.lK, this);
      Y.subscribe('remoteQueueChange', this.pg, this);
      Y.subscribe('previousNextChange', this.Sa, this);
      Y.subscribe('nowAutoplaying', this.Wf, this);
      Y.subscribe('autoplayDismissed', this.RT, this);
      g.b(this, this.j);
      g.b(this, this.X);
      g.b(this, this.Z);
      g.b(this, this.N);
      g.b(this, this.S);
      this.dN();
      this.pg();
      this.lK();
    },
    MgX = function (Y, u) {
      if (ff(Y)) {
        Y.YV.unsubscribe('remotePlayerChange', Y.lK, Y);
        var n = Math.round(u.volume);
        u = !!u.muted;
        var U = bi(Y.YV);
        if (n !== U.volume || u !== U.muted) (Y.YV.setVolume(n, u), Y.N.start());
        Y.YV.subscribe('remotePlayerChange', Y.lK, Y);
      }
    },
    Gnq = function (Y) {
      Y.ye(0);
      Y.j.stop();
      Y.t_(new g.RZ(64));
    },
    Alu = function (Y, u) {
      if (ff(Y) && !Y.J) {
        var n = null;
        u && ((n = { style: Y.L.getSubtitlesUserSettings() }), Object.assign(n, u));
        Y.YV.pS(Y.L.getVideoData(1).videoId, n);
        Y.G = bi(Y.YV).trackData;
      }
    },
    QG = function (Y, u) {
      var n = Y.L.getPlaylist();
      if (n == null ? 0 : n.listId) {
        var U = n.index;
        var k = n.listId.toString();
      }
      n = Y.L.getVideoData(1);
      Y.YV.playVideo(n.videoId, u, U, k, n.playerParams, n.Fk, no$(n));
      Y.t_(new g.RZ(1));
    },
    jb$ = function (Y, u) {
      if (u) {
        var n = Y.L.getOption('captions', 'tracklist', { p9: 1 });
        n && n.length
          ? (Y.L.setOption('captions', 'track', u), (Y.J = !1))
          : (Y.L.loadModule('captions'), (Y.J = !0));
      } else Y.L.setOption('captions', 'track', {});
    },
    ff = function (Y) {
      return bi(Y.YV).videoId === Y.L.getVideoData(1).videoId;
    },
    KCJ = function (Y, u) {
      g.qa.call(this, Y);
      this.K = u;
    },
    N6 = function () {
      g.H.call(this, {
        D: 'div',
        C: 'ytp-mdx-popup-dialog',
        T: { role: 'dialog' },
        U: [
          {
            D: 'div',
            C: 'ytp-mdx-popup-dialog-inner-content',
            U: [
              { D: 'div', C: 'ytp-mdx-popup-title', RV: 'Niste prijavljeni' },
              {
                D: 'div',
                C: 'ytp-mdx-popup-description',
                RV: 'Videoposnetki, ki jih gledate, bodo morda dodani v zgodovino ogledov v televizorju in bodo vplivali na priporo\u010dila za televizor. Temu se izognete tako, da prekli\u010dete in se prijavite v YouTube v svojem ra\u010dunalniku.',
              },
              {
                D: 'div',
                C: 'ytp-mdx-privacy-popup-buttons',
                U: [
                  {
                    D: 'button',
                    Oc: ['ytp-button', 'ytp-mdx-privacy-popup-cancel'],
                    RV: 'Prekli\u010di',
                  },
                  {
                    D: 'button',
                    Oc: ['ytp-button', 'ytp-mdx-privacy-popup-confirm'],
                    RV: 'Potrdi',
                  },
                ],
              },
            ],
          },
        ],
      });
      this.fade = new g.Je(this, 250);
      this.cancelButton = this.Xk('ytp-mdx-privacy-popup-cancel');
      this.confirmButton = this.Xk('ytp-mdx-privacy-popup-confirm');
      g.b(this, this.fade);
      this.B(this.cancelButton, 'click', this.K);
      this.B(this.confirmButton, 'click', this.j);
    },
    ip = function (Y) {
      g.H.call(this, {
        D: 'div',
        C: 'ytp-remote',
        U: [
          {
            D: 'div',
            C: 'ytp-remote-display-status',
            U: [
              { D: 'div', C: 'ytp-remote-display-status-icon', U: [g.S20()] },
              { D: 'div', C: 'ytp-remote-display-status-text', RV: '{{statustext}}' },
            ],
          },
        ],
      });
      this.api = Y;
      this.fade = new g.Je(this, 250);
      g.b(this, this.fade);
      this.B(Y, 'presentingplayerstatechange', this.onStateChange);
      this.Ve(Y.getPlayerStateObject());
    },
    Zc = function (Y, u) {
      g.gJ.call(this, 'Predvajaj v', 1, Y, u);
      this.L = Y;
      this.K6 = {};
      this.B(Y, 'onMdxReceiversChange', this.G);
      this.B(Y, 'presentingplayerstatechange', this.G);
      this.G();
    },
    prB = function (Y) {
      g.vH.call(this, Y);
      this.tG = { key: HvJ(), name: 'Tem ra\u010dunalniku' };
      this.v2 = null;
      this.subscriptions = [];
      this.gR = this.YV = null;
      this.K6 = [this.tG];
      this.zY = this.tG;
      this.Zk = new g.RZ(64);
      this.jd = 0;
      this.oM = -1;
      this.Nj = !1;
      this.RM = this.Uk = this.Tk = null;
      if (!g.CV(this.player.Y()) && !g.R8(this.player.Y())) {
        Y = this.player;
        var u = g.w6(Y);
        u && (u = u.jc()) && ((u = new Zc(Y, u)), g.b(this, u));
        u = new ip(Y);
        g.b(this, u);
        g.uc(Y, u.element, 4);
        this.Tk = new N6();
        g.b(this, this.Tk);
        g.uc(Y, this.Tk.element, 4);
        this.Nj = !!UO();
      }
    },
    TV = function (Y) {
      Y.Uk && (Y.player.removeEventListener('presentingplayerstatechange', Y.Uk), (Y.Uk = null));
    },
    LCq = function (Y, u, n) {
      Y.Zk = n;
      Y.player.publish('presentingplayerstatechange', new g.PY(n, u));
    },
    rQ = function (Y, u) {
      if (u.key !== Y.zY.key)
        if (u.key === Y.tG.key) PE();
        else if (
          (sb$(Y) && tgG(Y),
          (Y.zY = u),
          !Y.player.Y().V('disable_mdx_connection_in_mdx_module_for_music_web') ||
            !g.R8(Y.player.Y()))
        ) {
          var n = Y.player.getPlaylistId();
          var U = Y.player.getVideoData(1);
          var k = U.videoId;
          if (
            (!n && !k) ||
            ((Y.player.getAppState() === 2 || Y.player.getAppState() === 1) &&
              Y.player.Y().V('should_clear_video_data_on_player_cued_unstarted'))
          )
            U = null;
          else {
            var m = Y.player.getPlaylist();
            if (m) {
              var X = [];
              for (var S = 0; S < m.length; S++) X[S] = g.BH(m, S).videoId;
            } else X = [k];
            m = Y.player.getCurrentTime(1);
            Y = {
              videoIds: X,
              listId: n,
              videoId: k,
              playerParams: U.playerParams,
              clickTrackingParams: U.Fk,
              index: Math.max(Y.player.getPlaylistIndex(), 0),
              currentTime: m === 0 ? void 0 : m,
            };
            (U = no$(U)) && (Y.locationInfo = U);
            U = Y;
          }
          YZ('Connecting to: ' + g.zE(u));
          u.key == 'cast-selector-receiver'
            ? (nf(U || null),
              (u = U || null),
              vs() ? og().setLaunchParams(u) : Bs('setLaunchParams called before ready.'))
            : !U && iC$() && $t() == u.key
              ? MC('yt-remote-connection-change', !0)
              : (PE(), nf(U || null), (U = ag().XS()), (u = NC(U, u.key)) && S5(u, 1));
        }
    },
    sb$ = function (Y) {
      var u = Y.player.Y();
      return !u.V('mdx_enable_privacy_disclosure_ui') || Y.isLoggedIn() || Y.Nj || !Y.Tk
        ? !1
        : g.KV(u) || g.tA(u);
    },
    tgG = function (Y) {
      Y.player.getPlayerStateObject().isPlaying()
        ? Y.player.pauseVideo()
        : ((Y.Uk = function (u) {
            !Y.Nj && g.C1(u, 8) && (Y.player.pauseVideo(), TV(Y));
          }),
          Y.player.addEventListener('presentingplayerstatechange', Y.Uk));
      Y.Tk && Y.Tk.Su();
      mE() || (Cf = !0);
    };
  g.Vs.prototype.O8 = g.ke(49, function () {
    this.app.Dy().O8();
  });
  g.nd.prototype.O8 = g.ke(48, function () {
    this.RM = null;
  });
  g.Vs.prototype.wB = g.ke(47, function (Y) {
    this.app.Dy().wB(Y);
  });
  g.nd.prototype.wB = g.ke(46, function (Y) {
    this.RM = Y;
  });
  PL$.prototype.i8 = function (Y) {
    this.K.pu('/client_streamz/youtube/living_room/mdx/channel/opened', Y);
  };
  SUL.prototype.i8 = function (Y) {
    this.K.pu('/client_streamz/youtube/living_room/mdx/channel/closed', Y);
  };
  CLX.prototype.i8 = function (Y) {
    this.K.pu('/client_streamz/youtube/living_room/mdx/channel/message_received', Y);
  };
  fzL.prototype.i8 = function () {
    this.K.pu('/client_streamz/youtube/living_room/mdx/channel/success');
  };
  QoX.prototype.i8 = function (Y, u) {
    this.K.pu('/client_streamz/youtube/living_room/mdx/channel/error', Y, u);
  };
  NLR.prototype.i8 = function () {
    this.K.pu('/client_streamz/youtube/living_room/mdx/browser_channel/pending_maps');
  };
  ivJ.prototype.i8 = function () {
    this.K.pu('/client_streamz/youtube/living_room/mdx/browser_channel/undelivered_maps');
  };
  g.M = XP.prototype;
  g.M.RA = function () {
    Pz(this);
    for (var Y = [], u = 0; u < this.K.length; u++) Y.push(this.j[this.K[u]]);
    return Y;
  };
  g.M.Vv = function () {
    Pz(this);
    return this.K.concat();
  };
  g.M.has = function (Y) {
    return mp(this.j, Y);
  };
  g.M.equals = function (Y, u) {
    if (this === Y) return !0;
    if (this.size != Y.size) return !1;
    u = u || rkC;
    Pz(this);
    for (var n, U = 0; (n = this.K[U]); U++) if (!u(this.get(n), Y.get(n))) return !1;
    return !0;
  };
  g.M.isEmpty = function () {
    return this.size == 0;
  };
  g.M.clear = function () {
    this.j = {};
    this.Qc = this.size = this.K.length = 0;
  };
  g.M.remove = function (Y) {
    return this.delete(Y);
  };
  g.M.delete = function (Y) {
    return mp(this.j, Y)
      ? (delete this.j[Y], --this.size, this.Qc++, this.K.length > 2 * this.size && Pz(this), !0)
      : !1;
  };
  g.M.get = function (Y, u) {
    return mp(this.j, Y) ? this.j[Y] : u;
  };
  g.M.set = function (Y, u) {
    mp(this.j, Y) || ((this.size += 1), this.K.push(Y), this.Qc++);
    this.j[Y] = u;
  };
  g.M.forEach = function (Y, u) {
    for (var n = this.Vv(), U = 0; U < n.length; U++) {
      var k = n[U],
        m = this.get(k);
      Y.call(u, m, k, this);
    }
  };
  g.M.clone = function () {
    return new XP(this);
  };
  g.M.keys = function () {
    return g.M8(this.YO(!0)).K();
  };
  g.M.values = function () {
    return g.M8(this.YO(!1)).K();
  };
  g.M.entries = function () {
    var Y = this;
    return TLq(this.keys(), function (u) {
      return [u, Y.get(u)];
    });
  };
  g.M.YO = function (Y) {
    Pz(this);
    var u = 0,
      n = this.Qc,
      U = this,
      k = new g.j$();
    k.next = function () {
      if (n != U.Qc) throw Error('The map has changed since the iterator was created');
      if (u >= U.K.length) return g.i1;
      var m = U.K[u++];
      return g.Kc(Y ? m : U.j[m]);
    };
    return k;
  };
  var GqX = {
      OFV: 'atp',
      tUk: 'ska',
      D$g: 'que',
      VlG: 'mus',
      m$q: 'sus',
      ovG: 'dsp',
      kGk: 'seq',
      LNV: 'mic',
      DYg: 'dpa',
      Mlk: 'mlm',
      u$g: 'dsdtr',
      ZuG: 'ntb',
      eAz: 'vsp',
      C4c: 'scn',
      LGW: 'rpe',
      jOJ: 'dcn',
      Xdw: 'dcp',
      aTw: 'pas',
      qeF: 'drq',
      w2w: 'opf',
      SeW: 'els',
      VQz: 'isg',
      ElJ: 'svq',
      JU2: 'mvp',
      FTG: 'ads',
      fbc: 'stcp',
      wDF: 'sads',
      Gg2: 'dloc',
      Lm2: 'dcw',
      WTk: 'asw',
      Haa: 'apw',
    },
    AkX = { QDq: 'u', dX2: 'cl', mIZ: 'k', Fa2: 'i', Iyc: 'cr', SCG: 'm', TOc: 'g', DJ: 'up' },
    m3q = { Nm: 'adPlaying', IW: 'onAdStateChange' },
    XNy = {
      EOk: 'nowPlaying',
      zKZ: 'onStateChange',
      Nm: 'adPlaying',
      IW: 'onAdStateChange',
      Ns: 'nowPlayingShorts',
      Kj: 'onShortsStateChange',
    },
    PDX = { Ns: 'nowPlayingShorts', Kj: 'onShortsStateChange' };
  SY.prototype.equals = function (Y) {
    return Y ? this.id == Y.id : !1;
  };
  var qUQ = '',
    r_ = null;
  g.d(mxC, g.xA);
  var s1,
    ibB = PWJ('loadCastFramework') || PWJ('loadCastApplicationFramework'),
    r6q = ['pkedcjkdefgpdelpbcmbmeomcjbeemfm', 'enhhojjnijigcajfphajepfemndkmdlo'];
  g.T$(Gx, g.e);
  g.M = Gx.prototype;
  g.M.Ga = function (Y) {
    this.G = arguments;
    this.K = !1;
    this.C0 ? (this.X = g.iQ() + this.Qu) : (this.C0 = g.WB(this.J, this.Qu));
  };
  g.M.stop = function () {
    this.C0 && (g.$e.clearTimeout(this.C0), (this.C0 = null));
    this.X = null;
    this.K = !1;
    this.G = [];
  };
  g.M.pause = function () {
    ++this.j;
  };
  g.M.resume = function () {
    this.j && (--this.j, !this.j && this.K && ((this.K = !1), this.W.apply(null, this.G)));
  };
  g.M.nG = function () {
    this.stop();
    Gx.PM.nG.call(this);
  };
  g.M.uj = function () {
    this.C0 && (g.$e.clearTimeout(this.C0), (this.C0 = null));
    this.X
      ? ((this.C0 = g.WB(this.J, this.X - g.iQ())), (this.X = null))
      : this.j
        ? (this.K = !0)
        : ((this.K = !1), this.W.apply(null, this.G));
  };
  Ai.prototype.stringify = function (Y) {
    return g.$e.JSON.stringify(Y, void 0);
  };
  Ai.prototype.parse = function (Y) {
    return g.$e.JSON.parse(Y, void 0);
  };
  g.T$(sUg, g.Vy);
  g.T$(dxX, g.Vy);
  var GPX = null;
  g.T$(jUB, g.Vy);
  g.T$(KHg, g.Vy);
  g.T$(pkG, g.Vy);
  L8.prototype.debug = function () {};
  L8.prototype.info = function () {};
  L8.prototype.warning = function () {};
  var Dxg = {},
    ReG = {};
  g.M = ti.prototype;
  g.M.setTimeout = function (Y) {
    this.Pz = Y;
  };
  g.M.DS = function (Y) {
    Y = Y.target;
    var u = this.zZ;
    u && g.O6(Y) == 3 ? u.pw() : this.LS(Y);
  };
  g.M.LS = function (Y) {
    try {
      if (Y == this.K)
        a: {
          var u = g.O6(this.K),
            n = this.K.j,
            U = this.K.getStatus();
          if (!(u < 3) && (u != 3 || (this.K && (this.j.X || g.JH(this.K) || g.qE(this.K))))) {
            this.MF || u != 4 || n == 7 || (n == 8 || U <= 0 ? jY(3) : jY(2));
            heL(this);
            var k = this.K.getStatus();
            this.Ru = k;
            var m = vUJ(this);
            if ((this.W = k == 200)) {
              if (this.nT && !this.CG) {
                b: {
                  if (this.K) {
                    var X = g.a1(this.K, 'X-HTTP-Initial-Response');
                    if (X && !g.vq(X)) {
                      var S = X;
                      break b;
                    }
                  }
                  S = null;
                }
                if ((Y = S)) ((this.CG = !0), Hbg(this, Y));
                else {
                  this.W = !1;
                  this.J = 3;
                  K8(12);
                  oO(this);
                  cz(this);
                  break a;
                }
              }
              if (this.rg) {
                Y = !0;
                for (var C; !this.MF && this.S < m.length; )
                  if (((C = xxC(this, m)), C == ReG)) {
                    u == 4 && ((this.J = 4), K8(14), (Y = !1));
                    break;
                  } else if (C == Dxg) {
                    this.J = 4;
                    K8(15);
                    Y = !1;
                    break;
                  } else Hbg(this, C);
                c6u(this) && this.S != 0 && ((this.j.K = this.j.K.slice(this.S)), (this.S = 0));
                u != 4 || m.length != 0 || this.j.X || ((this.J = 1), K8(16), (Y = !1));
                this.W = this.W && Y;
                Y
                  ? m.length > 0 && !this.Gw && ((this.Gw = !0), this.X.ZD(this))
                  : (oO(this), cz(this));
              } else Hbg(this, m);
              u == 4 && oO(this);
              this.W && !this.MF && (u == 4 ? wkR(this.X, this) : ((this.W = !1), Bz(this)));
            } else
              (g.M$c(this.K),
                k == 400 && m.indexOf('Unknown SID') > 0
                  ? ((this.J = 3), K8(12))
                  : ((this.J = 0), K8(13)),
                oO(this),
                cz(this));
          }
        }
    } catch (f) {
    } finally {
    }
  };
  g.M.cancel = function () {
    this.MF = !0;
    oO(this);
  };
  g.M.rT = function () {
    this.KG = null;
    var Y = Date.now();
    Y - this.Uc >= 0
      ? (this.JJ != 2 && (jY(3), K8(17)), oO(this), (this.J = 2), cz(this))
      : lmB(this, this.Uc - Y);
  };
  g.M.getLastError = function () {
    return this.J;
  };
  g.M.YJ = function () {
    return this.K;
  };
  Vog.prototype.cancel = function () {
    this.X = FHq(this);
    if (this.j) (this.j.cancel(), (this.j = null));
    else if (this.K && this.K.size !== 0) {
      for (var Y = g.A(this.K.values()), u = Y.next(); !u.done; u = Y.next()) u.value.cancel();
      this.K.clear();
    }
  };
  g.M = $xG.prototype;
  g.M.OB = 8;
  g.M.EE = 1;
  g.M.connect = function (Y, u, n, U) {
    K8(0);
    this.CT = Y;
    this.MF = u || {};
    n && U !== void 0 && ((this.MF.OSID = n), (this.MF.OAID = U));
    this.CG = this.Qm;
    this.Fk = zeQ(this, null, this.CT);
    x2(this);
  };
  g.M.disconnect = function () {
    uQG(this);
    if (this.EE == 3) {
      var Y = this.TZ++,
        u = this.Fk.clone();
      g.Qp(u, 'SID', this.G);
      g.Qp(u, 'RID', Y);
      g.Qp(u, 'TYPE', 'terminate');
      w_(this, u);
      Y = new ti(this, this.G, Y);
      Y.JJ = 2;
      Y.Z = uE(u.clone());
      u = !1;
      if (g.$e.navigator && g.$e.navigator.sendBeacon)
        try {
          u = g.$e.navigator.sendBeacon(Y.Z.toString(), '');
        } catch (n) {}
      !u && g.$e.Image && ((new Image().src = Y.Z), (u = !0));
      u || ((Y.K = oUC(Y.X, null)), Y.K.send(Y.Z));
      Y.jG = Date.now();
      Bz(Y);
    }
    PUy(this);
  };
  g.M.cW = function () {
    return this.EE == 0;
  };
  g.M.getState = function () {
    return this.EE;
  };
  g.M.HO = function (Y) {
    if (this.W)
      if (((this.W = null), this.EE == 1)) {
        if (!Y) {
          this.TZ = Math.floor(Math.random() * 1e5);
          Y = this.TZ++;
          var u = new ti(this, '', Y),
            n = this.N;
          this.Ru && (n ? ((n = g.rc(n)), g.sF(n, this.Ru)) : (n = this.Ru));
          this.S !== null || this.Uc || ((u.Fk = n), (n = null));
          var U;
          if (this.Iu)
            a: {
              for (var k = (U = 0); k < this.X.length; k++) {
                b: {
                  var m = this.X[k];
                  if ('__data__' in m.map && ((m = m.map.__data__), typeof m === 'string')) {
                    m = m.length;
                    break b;
                  }
                  m = void 0;
                }
                if (m === void 0) break;
                U += m;
                if (U > 4096) {
                  U = k;
                  break a;
                }
                if (U === 4096 || k === this.X.length - 1) {
                  U = k + 1;
                  break a;
                }
              }
              U = 1e3;
            }
          else U = 1e3;
          U = kCQ(this, u, U);
          k = this.Fk.clone();
          g.Qp(k, 'RID', Y);
          g.Qp(k, 'CVER', 22);
          this.rg && g.Qp(k, 'X-HTTP-Session-Id', this.rg);
          w_(this, k);
          n &&
            (this.Uc ? (U = 'headers=' + g.oD(g.eFM(n)) + '&' + U) : this.S && g.TL(k, this.S, n));
          ImX(this.j, u);
          this.VI && g.Qp(k, 'TYPE', 'init');
          this.Iu
            ? (g.Qp(k, '$req', U), g.Qp(k, 'SID', 'null'), (u.nT = !0), BTR(u, k, null))
            : BTR(u, k, U);
          this.EE = 2;
        }
      } else this.EE == 3 && (Y ? myX(this, Y) : this.X.length == 0 || ObJ(this.j) || myX(this));
  };
  g.M.FQ = function () {
    this.Z = null;
    XFR(this);
    if (this.eE && !(this.Pz || this.K == null || this.uD <= 0)) {
      var Y = 4 * this.uD;
      this.DW = p8((0, g.fR)(this.e2a, this), Y);
    }
  };
  g.M.e2a = function () {
    this.DW && ((this.DW = null), (this.CG = !1), (this.Pz = !0), K8(10), RO(this), XFR(this));
  };
  g.M.ZD = function (Y) {
    this.K == Y && this.eE && !this.Pz && (Y$L(this), (this.Pz = !0), K8(11));
  };
  g.M.y8 = function () {
    this.KG != null && ((this.KG = null), RO(this), eeL(this), K8(19));
  };
  g.M.gQc = function (Y) {
    Y ? K8(2) : K8(1);
  };
  g.M.isActive = function () {
    return !!this.J && this.J.isActive(this);
  };
  g.M = CU$.prototype;
  g.M.MZ = function () {};
  g.M.gQ = function () {};
  g.M.A0 = function () {};
  g.M.WO = function () {};
  g.M.isActive = function () {
    return !0;
  };
  g.M.Lv = function () {};
  g.T$(eY, g.is);
  eY.prototype.open = function () {
    this.K.J = this.X;
    this.W && (this.K.JJ = !0);
    this.K.connect(this.J, this.j || void 0);
  };
  eY.prototype.close = function () {
    this.K.disconnect();
  };
  eY.prototype.send = function (Y) {
    var u = this.K;
    if (typeof Y === 'string') {
      var n = {};
      n.__data__ = Y;
      Y = n;
    } else this.G && ((n = {}), (n.__data__ = g.zE(Y)), (Y = n));
    u.X.push(new y6u(u.kQ++, Y));
    u.EE == 3 && x2(u);
  };
  eY.prototype.nG = function () {
    this.K.J = null;
    delete this.X;
    this.K.disconnect();
    delete this.K;
    eY.PM.nG.call(this);
  };
  g.T$(QRX, sUg);
  g.T$(NDg, dxX);
  g.T$(Wz, CU$);
  Wz.prototype.MZ = function () {
    this.K.dispatchEvent('m');
  };
  Wz.prototype.gQ = function (Y) {
    this.K.dispatchEvent(new QRX(Y));
  };
  Wz.prototype.A0 = function (Y) {
    this.K.dispatchEvent(new NDg(Y));
  };
  Wz.prototype.WO = function () {
    this.K.dispatchEvent('n');
  };
  var IO = new g.is();
  g.d(TDJ, g.Vy);
  g.M = g_.prototype;
  g.M.zN = null;
  g.M.HS = !1;
  g.M.O7 = null;
  g.M.YF = null;
  g.M.oQ = null;
  g.M.QU = null;
  g.M.xP = null;
  g.M.B6 = null;
  g.M.Yq = null;
  g.M.fU = null;
  g.M.eX = 0;
  g.M.Rd = null;
  g.M.Z5 = null;
  g.M.TN = null;
  g.M.KM = -1;
  g.M.a$ = !0;
  g.M.IQ = !1;
  g.M.Tb = 0;
  g.M.kh = null;
  var AEX = {},
    GC$ = {};
  g.M = g_.prototype;
  g.M.setTimeout = function (Y) {
    this.j = Y;
  };
  g.M.Fv = function (Y) {
    Y = Y.target;
    var u = this.kh;
    u && g.O6(Y) == 3 ? u.pw() : this.J0(Y);
  };
  g.M.J0 = function (Y) {
    try {
      if (Y == this.fU)
        a: {
          var u = g.O6(this.fU),
            n = this.fU.j,
            U = this.fU.getStatus();
          if (g.NK && !g.zr('420+')) {
            if (u < 4) break a;
          } else if (u < 3 || (u == 3 && !g.JH(this.fU))) break a;
          this.IQ || u != 4 || n == 7 || (n == 8 || U <= 0 ? this.K.Sn(3) : this.K.Sn(2));
          pFy(this);
          var k = this.fU.getStatus();
          this.KM = k;
          var m = g.JH(this.fU);
          if ((this.HS = k == 200)) {
            u == 4 && E1(this);
            if (this.rg) {
              for (Y = !0; !this.IQ && this.eX < m.length; ) {
                var X = jRu(this, m);
                if (X == GC$) {
                  u == 4 && ((this.TN = 4), zx(15), (Y = !1));
                  break;
                } else if (X == AEX) {
                  this.TN = 4;
                  zx(16);
                  Y = !1;
                  break;
                } else t2G(this, X);
              }
              u == 4 && m.length == 0 && ((this.TN = 1), zx(17), (Y = !1));
              this.HS = this.HS && Y;
              Y || (E1(this), LhR(this));
            } else t2G(this, m);
            this.HS && !this.IQ && (u == 4 ? this.K.mH(this) : ((this.HS = !1), dyX(this)));
          } else
            (k == 400 && m.indexOf('Unknown SID') > 0
              ? ((this.TN = 3), zx(13))
              : ((this.TN = 0), zx(14)),
              E1(this),
              LhR(this));
        }
    } catch (S) {
    } finally {
    }
  };
  g.M.cancel = function () {
    this.IQ = !0;
    E1(this);
  };
  g.M.OM = function () {
    this.O7 = null;
    var Y = Date.now();
    Y - this.YF >= 0
      ? (this.QU != 2 && this.K.Sn(3), E1(this), (this.TN = 2), zx(18), LhR(this))
      : Kh$(this, this.YF - Y);
  };
  g.M.getLastError = function () {
    return this.TN;
  };
  g.M = cE$.prototype;
  g.M.PU = null;
  g.M.sT = null;
  g.M.OR = !1;
  g.M.sL = null;
  g.M.EC = null;
  g.M.dM = -1;
  g.M.Ew = null;
  g.M.Un = null;
  g.M.connect = function (Y) {
    this.sL = Y;
    Y = yo(this.K, null, this.sL);
    zx(3);
    Date.now();
    var u = this.K.N;
    u != null
      ? ((this.Ew = u[0]),
        (this.Un = u[1]) ? ((this.EC = 1), va$(this)) : ((this.EC = 2), R3$(this)))
      : (n8(Y, 'MODE', 'init'),
        (this.sT = new g_(this)),
        (this.sT.zN = this.PU),
        sRB(this.sT, Y, !1, null, !0),
        (this.EC = 0));
  };
  g.M.t5 = function (Y) {
    if (Y) ((this.EC = 2), R3$(this));
    else {
      zx(4);
      var u = this.K;
      u.fd = u.wu.dM;
      Ji(u, 9);
    }
    Y && this.Sn(2);
  };
  g.M.vU = function (Y) {
    return this.K.vU(Y);
  };
  g.M.abort = function () {
    this.sT && (this.sT.cancel(), (this.sT = null));
    this.dM = -1;
  };
  g.M.cW = function () {
    return !1;
  };
  g.M.Vo = function (Y, u) {
    this.dM = Y.KM;
    if (this.EC == 0)
      if (u) {
        try {
          var n = this.j.parse(u);
        } catch (U) {
          Y = this.K;
          Y.fd = this.dM;
          Ji(Y, 2);
          return;
        }
        this.Ew = n[0];
        this.Un = n[1];
      } else ((Y = this.K), (Y.fd = this.dM), Ji(Y, 2));
    else
      this.EC == 2 &&
        (this.OR
          ? (zx(7), Date.now())
          : u == '11111'
            ? (zx(6),
              (this.OR = !0),
              Date.now(),
              (this.dM = 200),
              this.sT.cancel(),
              zx(12),
              Vo(this.K, this, !0))
            : (zx(8), Date.now(), (this.OR = !1)));
  };
  g.M.mH = function () {
    this.dM = this.sT.KM;
    if (this.sT.HS)
      this.EC == 0
        ? this.Un
          ? ((this.EC = 1), va$(this))
          : ((this.EC = 2), R3$(this))
        : this.EC == 2 &&
          (this.OR ? (zx(12), Vo(this.K, this, !0)) : (zx(11), Vo(this.K, this, !1)));
    else {
      this.EC == 0 ? zx(9) : this.EC == 2 && zx(10);
      var Y = this.K;
      this.sT.getLastError();
      Y.fd = this.dM;
      Ji(Y, 2);
    }
  };
  g.M.fM = function () {
    return this.K.fM();
  };
  g.M.isActive = function () {
    return this.K.isActive();
  };
  g.M.Sn = function (Y) {
    this.K.Sn(Y);
  };
  g.M = Dyy.prototype;
  g.M.d3 = null;
  g.M.RQ = null;
  g.M.Rm = null;
  g.M.PW = null;
  g.M.UL = null;
  g.M.d4 = null;
  g.M.SF = null;
  g.M.aB = null;
  g.M.nM = 0;
  g.M.WE = 0;
  g.M.dw = null;
  g.M.WS = null;
  g.M.wM = null;
  g.M.PL = null;
  g.M.wu = null;
  g.M.Mv = null;
  g.M.Wy = -1;
  g.M.CS = -1;
  g.M.fd = -1;
  g.M.Hy = 0;
  g.M.Fb = 0;
  g.M.vL = 8;
  var BU$ = {
    OK: 0,
    ApF: 2,
    X2g: 4,
    dSG: 5,
    BmF: 6,
    STOP: 7,
    Ud: 8,
    AVZ: 9,
    FYV: 10,
    WYk: 11,
    At2: 12,
  };
  g.T$(l0G, g.Vy);
  g.T$(h3C, g.Vy);
  g.M = Dyy.prototype;
  g.M.connect = function (Y, u, n, U, k) {
    zx(0);
    this.UL = u;
    this.RQ = n || {};
    U && k !== void 0 && ((this.RQ.OSID = U), (this.RQ.OAID = k));
    this.Z ? (bE((0, g.fR)(this.Nn, this, Y), 100), Whu(this)) : this.Nn(Y);
  };
  g.M.disconnect = function () {
    e3$(this);
    if (this.K == 3) {
      var Y = this.nM++,
        u = this.d4.clone();
      g.Qp(u, 'SID', this.G);
      g.Qp(u, 'RID', Y);
      g.Qp(u, 'TYPE', 'terminate');
      FP(this, u);
      Y = new g_(this, this.G, Y);
      Y.QU = 2;
      Y.xP = uE(u.clone());
      new Image().src = Y.xP.toString();
      Y.oQ = Date.now();
      dyX(Y);
    }
    FhX(this);
  };
  g.M.Nn = function (Y) {
    this.wu = new cE$(this);
    this.wu.PU = this.d3;
    this.wu.j = this.J;
    this.wu.connect(Y);
  };
  g.M.cW = function () {
    return this.K == 0;
  };
  g.M.getState = function () {
    return this.K;
  };
  g.M.im = function (Y) {
    this.WS = null;
    EaR(this, Y);
  };
  g.M.lm = function () {
    this.wM = null;
    this.PW = new g_(this, this.G, 'rpc', this.S);
    this.PW.zN = this.d3;
    this.PW.Tb = 0;
    var Y = this.SF.clone();
    g.Qp(Y, 'RID', 'rpc');
    g.Qp(Y, 'SID', this.G);
    g.Qp(Y, 'CI', this.Mv ? '0' : '1');
    g.Qp(Y, 'AID', this.Wy);
    FP(this, Y);
    g.Qp(Y, 'TYPE', 'xmlhttp');
    sRB(this.PW, Y, !0, this.aB, !1);
  };
  g.M.Vo = function (Y, u) {
    if (this.K != 0 && (this.PW == Y || this.Rm == Y))
      if (((this.fd = Y.KM), this.Rm == Y && this.K == 3))
        if (this.vL > 7) {
          try {
            var n = this.J.parse(u);
          } catch (U) {
            n = null;
          }
          if (Array.isArray(n) && n.length == 3)
            if (((Y = n), Y[0] == 0))
              a: {
                if (!this.wM) {
                  if (this.PW)
                    if (this.PW.oQ + 3e3 < this.Rm.oQ)
                      (O1(this), this.PW.cancel(), (this.PW = null));
                    else break a;
                  V2Q(this);
                  zx(19);
                }
              }
            else
              ((this.CS = Y[1]),
                0 < this.CS - this.Wy &&
                  Y[2] < 37500 &&
                  this.Mv &&
                  this.Fb == 0 &&
                  !this.PL &&
                  (this.PL = bE((0, g.fR)(this.AX, this), 6e3)));
          else Ji(this, 11);
        } else u != 'y2f%' && Ji(this, 11);
      else if ((this.PW == Y && O1(this), !g.vq(u)))
        for (Y = this.J.parse(u), u = 0; u < Y.length; u++)
          ((n = Y[u]),
            (this.Wy = n[0]),
            (n = n[1]),
            this.K == 2
              ? n[0] == 'c'
                ? ((this.G = n[1]),
                  (this.aB = n[2]),
                  (n = n[3]),
                  n != null ? (this.vL = n) : (this.vL = 6),
                  (this.K = 3),
                  this.dw && this.dw.Qo(),
                  (this.SF = yo(this, this.fM() ? this.aB : null, this.UL)),
                  HX$(this))
                : n[0] == 'stop' && Ji(this, 7)
              : this.K == 3 &&
                (n[0] == 'stop' ? Ji(this, 7) : n[0] != 'noop' && this.dw && this.dw.BO(n),
                (this.Fb = 0)));
  };
  g.M.AX = function () {
    this.PL != null && ((this.PL = null), this.PW.cancel(), (this.PW = null), V2Q(this), zx(20));
  };
  g.M.mH = function (Y) {
    if (this.PW == Y) {
      O1(this);
      this.PW = null;
      var u = 2;
    } else if (this.Rm == Y) ((this.Rm = null), (u = 1));
    else return;
    this.fd = Y.KM;
    if (this.K != 0)
      if (Y.HS)
        if (u == 1) {
          u = Y.Yq ? Y.Yq.length : 0;
          Y = Date.now() - Y.oQ;
          var n = IO;
          n.dispatchEvent(new l0G(n, u, Y, this.Hy));
          wFu(this);
          this.dw && this.dw.Zm(this, this.X);
          this.X.length = 0;
        } else HX$(this);
      else {
        n = Y.getLastError();
        var U;
        if (!(U = n == 3 || n == 7 || (n == 0 && this.fd > 0))) {
          if ((U = u == 1))
            this.Rm || this.WS || this.K == 1 || this.Hy >= 2
              ? (U = !1)
              : ((this.WS = bE((0, g.fR)(this.im, this, Y), yE$(this, this.Hy))),
                this.Hy++,
                (U = !0));
          U = !(U || (u == 2 && V2Q(this)));
        }
        if (U)
          switch (n) {
            case 1:
              Ji(this, 5);
              break;
            case 4:
              Ji(this, 10);
              break;
            case 3:
              Ji(this, 6);
              break;
            case 7:
              Ji(this, 12);
              break;
            default:
              Ji(this, 2);
          }
      }
  };
  g.M.HE = function (Y) {
    if (!g.jB(arguments, this.K)) throw Error('Unexpected channel state: ' + this.K);
  };
  g.M.Abq = function (Y) {
    Y ? zx(2) : (zx(1), OX$(this, 8));
  };
  g.M.vU = function (Y) {
    if (Y) throw Error("Can't create secondary domain capable XhrIo object.");
    Y = new g.HB();
    Y.S = !1;
    return Y;
  };
  g.M.isActive = function () {
    return !!this.dw && this.dw.isActive(this);
  };
  g.M.Sn = function (Y) {
    var u = IO;
    u.dispatchEvent(new h3C(u, Y));
  };
  g.M.fM = function () {
    return !1;
  };
  g.M = JE$.prototype;
  g.M.Qo = function () {};
  g.M.BO = function () {};
  g.M.Zm = function () {};
  g.M.kN = function () {};
  g.M.Nv = function () {};
  g.M.eF = function () {
    return {};
  };
  g.M.isActive = function () {
    return !0;
  };
  g.M = q$$.prototype;
  g.M.enqueue = function (Y) {
    this.j.push(Y);
  };
  g.M.isEmpty = function () {
    return this.K.length === 0 && this.j.length === 0;
  };
  g.M.clear = function () {
    this.K = [];
    this.j = [];
  };
  g.M.contains = function (Y) {
    return g.jB(this.K, Y) || g.jB(this.j, Y);
  };
  g.M.remove = function (Y) {
    var u = this.K;
    var n = (0, g.B$Q)(u, Y);
    n >= 0 ? (g.KR(u, n), (u = !0)) : (u = !1);
    return u || g.pR(this.j, Y);
  };
  g.M.RA = function () {
    for (var Y = [], u = this.K.length - 1; u >= 0; --u) Y.push(this.K[u]);
    u = this.j.length;
    for (var n = 0; n < u; ++n) Y.push(this.j[n]);
    return Y;
  };
  g.d(a0q, g.Vy);
  g.d($yg, g.Vy);
  g.T$(qC, g.e);
  g.M = qC.prototype;
  g.M.bsG = function () {
    this.Qu = Math.min(3e5, this.Qu * 2);
    this.X();
    this.j && this.start();
  };
  g.M.start = function () {
    var Y = this.Qu + 15e3 * Math.random();
    g.OQ(this.K, Y);
    this.j = Date.now() + Y;
  };
  g.M.stop = function () {
    this.K.stop();
    this.j = 0;
  };
  g.M.isActive = function () {
    return this.K.isActive();
  };
  g.M.reset = function () {
    this.K.stop();
    this.Qu = 5e3;
  };
  g.T$(uu$, JE$);
  g.M = uu$.prototype;
  g.M.subscribe = function (Y, u, n) {
    return this.W.subscribe(Y, u, n);
  };
  g.M.unsubscribe = function (Y, u, n) {
    return this.W.unsubscribe(Y, u, n);
  };
  g.M.eh = function (Y) {
    return this.W.eh(Y);
  };
  g.M.publish = function (Y, u) {
    return this.W.publish.apply(this.W, arguments);
  };
  g.M.dispose = function () {
    this.S ||
      ((this.S = !0),
      g.nc(this.W),
      this.disconnect(),
      g.nc(this.j),
      (this.j = null),
      (this.rg = function () {
        return '';
      }),
      (this.Fk = function () {
        return g.R1({});
      }));
  };
  g.M.gg = function () {
    return this.S;
  };
  g.M.connect = function (Y, u, n) {
    var U = this,
      k,
      m,
      X,
      S;
    return g.l(function (C) {
      if (C.j == 1) return (g.LY(C, 2), U.J ? g.D(C, U.G, 2) : C.qF(2));
      g.lB(C);
      if (U.S || (U.K && U.K.getState() == 2)) return C.return();
      U.jG = '';
      U.j.stop();
      U.N = Y || null;
      U.Z = u || 0;
      k = U.JJ + '/test';
      m = U.JJ + '/bind';
      X = new Dyy(n ? n.firstTestResults : null, n ? n.secondTestResults : null, U.Gw);
      if ((S = U.K)) S.dw = null;
      X.dw = U;
      U.K = X;
      if (U.J)
        return (
          (U.G = CD$(U).then(function () {
            return kl$(U, k, m, S, n);
          })),
          C.return(
            U.G.then(function () {
              U.G = g.R1();
            })
          )
        );
      kl$(U, k, m, S, n);
      return g.wG(C, 0);
    });
  };
  g.M.disconnect = function (Y) {
    try {
      this.J && (this.G.cancel(), (this.G = g.R1()));
    } finally {
      ((this.oV = Y || 0),
        this.j && this.j.stop(),
        nHQ(this),
        this.K && (this.K.getState() == 3 && EaR(this.K), this.K.disconnect()),
        (this.oV = 0));
    }
  };
  g.M.sendMessage = function (Y, u) {
    var n = this,
      U;
    return g.l(function (k) {
      switch (k.j) {
        case 1:
          g.LY(k, 2);
          if (!n.J) {
            k.qF(2);
            break;
          }
          return g.D(k, n.G, 2);
        case 2:
          g.lB(k);
          if (n.S) return k.return();
          U = { _sc: Y };
          u && g.sF(U, u);
          if (n.j.isActive() || (n.K ? n.K.getState() : 0) == 2) {
            n.X.push(U);
            k.qF(6);
            break;
          }
          if (!n.OZ()) {
            k.qF(6);
            break;
          }
          g.LY(k, 8);
          if (!n.J || S0q(n, Y)) {
            k.qF(8);
            break;
          }
          return g.D(k, CD$(n), 8);
        case 8:
          g.lB(k, 0, 0, 1);
          n.OZ() && (S0q(n, Y) || U3R(n), nHQ(n), bXR(n.K, U));
          g.wG(k, 6, 1);
          break;
        case 6:
          g.wG(k, 0);
      }
    });
  };
  g.M.Qo = function () {
    this.j.reset();
    this.N = null;
    this.Z = 0;
    if (this.X.length)
      if (this.J) Q9$(this);
      else {
        var Y = this.X;
        this.X = [];
        var u = Y.length;
        U3R(this);
        fX$(this, Y, u);
        aO(this);
      }
    else aO(this);
  };
  g.M.kN = function (Y) {
    var u = Y == 2 && this.K.fd == 401;
    Y == 4 || u || this.j.start();
    this.publish('handlerError', Y, u);
    u = Object.keys(BU$).find(function (n) {
      return BU$[n] === Y;
    });
    this.zZ.i8('BROWSER_CHANNEL', u != null ? u : 'UNKNOWN');
  };
  g.M.Nv = function (Y, u) {
    if (!this.j.isActive()) this.publish('handlerClosed');
    else if (u)
      for (var n = u.length, U = 0; U < n; ++U) {
        var k = u[U].map;
        k && this.X.push(k);
      }
    this.CG.i8('BROWSER_CHANNEL');
    Y &&
      this.eE.K.Ii(
        '/client_streamz/youtube/living_room/mdx/browser_channel/pending_maps',
        Y.length
      );
    u &&
      this.Ub.K.Ii(
        '/client_streamz/youtube/living_room/mdx/browser_channel/undelivered_maps',
        u.length
      );
  };
  g.M.Zm = function (Y, u) {
    u != null && Y != null && this.Pz.i8();
  };
  g.M.eF = function () {
    var Y = { v: 2 };
    this.jG && (Y.gsessionid = this.jG);
    this.Z != 0 && (Y.ui = '' + this.Z);
    this.oV != 0 && (Y.ui = '' + this.oV);
    this.N && g.sF(Y, this.N);
    return Y;
  };
  g.M.BO = function (Y) {
    Y[0] == 'S'
      ? (this.jG = Y[1])
      : Y[0] == 'gracefulReconnect'
        ? (this.j.start(), this.K.disconnect())
        : this.publish('handlerMessage', new Y0B(Y[0], Y[1]));
    this.TZ.i8('BROWSER_CHANNEL');
  };
  g.M.OZ = function () {
    return !!this.K && this.K.getState() == 3;
  };
  g.M.KL = function (Y) {
    (this.KG.loungeIdToken = Y) || this.j.stop();
    if (this.CT && this.K) {
      var u = this.K.d3 || {};
      Y ? (u['X-YouTube-LoungeId-Token'] = Y) : delete u['X-YouTube-LoungeId-Token'];
      this.K.d3 = u;
    }
  };
  g.M.getDeviceId = function () {
    return this.KG.id;
  };
  g.M.nf = function () {
    return this.j.isActive() ? this.j.j - Date.now() : NaN;
  };
  g.M.Jc = function () {
    var Y = this.j;
    g.FD(Y.K);
    Y.start();
  };
  g.M.VWa = function () {
    this.j.isActive();
    I0B(this.K) == 0 && this.connect(this.N, this.Z);
  };
  $2.prototype.sendRequest = function (Y, u, n, U, k, m, X) {
    Y = {
      format: m ? 'RAW' : 'JSON',
      method: Y,
      context: this,
      timeout: 5e3,
      withCredentials: !!X,
      onSuccess: g.QC(this.G, U, !m),
      onError: g.QC(this.X, k),
      onTimeout: g.QC(this.J, k),
    };
    n &&
      ((Y.postParams = n), (Y.headers = { 'Content-Type': 'application/x-www-form-urlencoded' }));
    return g.Ak(u, Y);
  };
  $2.prototype.G = function (Y, u, n, U) {
    u ? Y(U) : Y({ text: n.responseText });
  };
  $2.prototype.X = function (Y, u) {
    Y(Error('Request error: ' + u.status));
  };
  $2.prototype.J = function (Y) {
    Y(Error('request timed out'));
  };
  g.d(ZzX, g.is);
  g.M = ZzX.prototype;
  g.M.connect = function (Y, u, n) {
    this.P0.connect(Y, u, n);
  };
  g.M.disconnect = function (Y) {
    this.P0.disconnect(Y);
  };
  g.M.Jc = function () {
    this.P0.Jc();
  };
  g.M.getDeviceId = function () {
    return this.P0.getDeviceId();
  };
  g.M.nf = function () {
    return this.P0.nf();
  };
  g.M.OZ = function () {
    return this.P0.OZ();
  };
  g.M.gT = function () {
    this.dispatchEvent('channelOpened');
    var Y = this.P0,
      u = this.K;
    g.oU('yt-remote-session-browser-channel', {
      firstTestResults: [''],
      secondTestResults: !Y.K.Mv,
      sessionId: Y.K.G,
      arrayId: Y.K.Wy,
    });
    g.oU('yt-remote-session-screen-id', u);
    Y = iE();
    u = Zl();
    g.jB(Y, u) || Y.push(u);
    JkL(Y);
    azL();
  };
  g.M.onClosed = function () {
    this.dispatchEvent('channelClosed');
  };
  g.M.onMessage = function (Y) {
    this.dispatchEvent(new a0q(Y));
  };
  g.M.onError = function (Y) {
    this.dispatchEvent(new $yg(Y ? 1 : 0));
  };
  g.M.sendMessage = function (Y, u) {
    this.P0.sendMessage(Y, u);
  };
  g.M.KL = function (Y) {
    this.P0.KL(Y);
  };
  g.M.dispose = function () {
    this.P0.dispose();
  };
  g.M = Toy.prototype;
  g.M.connect = function (Y, u) {
    Y = Y === void 0 ? {} : Y;
    u = u === void 0 ? 0 : u;
    this.W !== 2 &&
      (this.X.stop(),
      (this.Z = Y),
      (this.S = u),
      Mvg(this),
      (Y = g.z6('ID_TOKEN'))
        ? (this.G['x-youtube-identity-token'] = Y)
        : delete this.G['x-youtube-identity-token'],
      this.K &&
        ((this.j.device = this.K.device),
        (this.j.name = this.K.name),
        (this.j.app = this.K.app),
        (this.j.id = this.K.id),
        this.K.fW2 && (this.j.mdxVersion = '' + this.K.fW2),
        this.K.theme && (this.j.theme = this.K.theme),
        this.K.capabilities && (this.j.capabilities = this.K.capabilities),
        this.K.uL && (this.j.cst = this.K.uL),
        this.K.authuser && (this.j.authuser = this.K.authuser),
        this.K.pageId && (this.j.pageId = this.K.pageId)),
      this.S !== 0 ? (this.j.ui = '' + this.S) : delete this.j.ui,
      Object.assign(this.j, this.Z),
      (this.channel = new eY(this.pathPrefix, { tF: 'gsessionid', bGV: this.G, jVW: this.j })),
      this.channel.open(),
      (this.W = 2),
      rDu(this));
  };
  g.M.disconnect = function (Y) {
    this.N = Y === void 0 ? 0 : Y;
    this.X.stop();
    Mvg(this);
    this.channel &&
      (this.N !== 0 ? (this.j.ui = '' + this.N) : delete this.j.ui, this.channel.close());
    this.N = 0;
  };
  g.M.nf = function () {
    return this.X.isActive() ? this.X.j - Date.now() : NaN;
  };
  g.M.Jc = function () {
    var Y = this.X;
    g.FD(Y.K);
    Y.start();
  };
  g.M.sendMessage = function (Y, u) {
    this.channel && (Mvg(this), (Y = Object.assign({}, { _sc: Y }, u)), this.channel.send(Y));
  };
  g.M.KL = function (Y) {
    Y || this.X.stop();
    Y ? (this.G['X-YouTube-LoungeId-Token'] = Y) : delete this.G['X-YouTube-LoungeId-Token'];
  };
  g.M.getDeviceId = function () {
    return this.K ? this.K.id : '';
  };
  g.M.publish = function (Y) {
    return this.J.publish.apply(this.J, [Y].concat(g.Zu(g.It.apply(1, arguments))));
  };
  g.M.subscribe = function (Y, u, n) {
    return this.J.subscribe(Y, u, n);
  };
  g.M.unsubscribe = function (Y, u, n) {
    return this.J.unsubscribe(Y, u, n);
  };
  g.M.eh = function (Y) {
    return this.J.eh(Y);
  };
  g.M.dispose = function () {
    this.KG ||
      ((this.KG = !0),
      g.nc(this.J),
      this.disconnect(),
      g.nc(this.X),
      (this.jG = function () {
        return '';
      }));
  };
  g.M.gg = function () {
    return this.KG;
  };
  g.d(s9L, g.is);
  g.M = s9L.prototype;
  g.M.connect = function (Y, u) {
    this.K.connect(Y, u);
  };
  g.M.disconnect = function (Y) {
    this.K.disconnect(Y);
  };
  g.M.Jc = function () {
    this.K.Jc();
  };
  g.M.getDeviceId = function () {
    return this.K.getDeviceId();
  };
  g.M.nf = function () {
    return this.K.nf();
  };
  g.M.OZ = function () {
    return this.K.W === 3;
  };
  g.M.Mu = function () {
    this.dispatchEvent('channelOpened');
  };
  g.M.onClosed = function () {
    this.dispatchEvent('channelClosed');
  };
  g.M.onMessage = function (Y) {
    this.dispatchEvent(new a0q(Y));
  };
  g.M.onError = function () {
    this.dispatchEvent(new $yg(this.K.Ab === 401 ? 1 : 0));
  };
  g.M.sendMessage = function (Y, u) {
    this.K.sendMessage(Y, u);
  };
  g.M.KL = function (Y) {
    this.K.KL(Y);
  };
  g.M.dispose = function () {
    this.K.dispose();
  };
  var tvy = Date.now(),
    ui = null,
    mY = Array(50),
    kt = -1,
    Xm = !1;
  g.T$(Ps, g.ud);
  Ps.prototype.XS = function () {
    return this.screens;
  };
  Ps.prototype.contains = function (Y) {
    return !!VsL(this.screens, Y);
  };
  Ps.prototype.get = function (Y) {
    return Y ? NC(this.screens, Y) : null;
  };
  Ps.prototype.info = function (Y) {
    ne(this.W, Y);
  };
  g.d(vH$, g.ud);
  g.M = vH$.prototype;
  g.M.start = function () {
    !this.K && isNaN(this.C0) && this.jA();
  };
  g.M.stop = function () {
    this.K && (this.K.abort(), (this.K = null));
    isNaN(this.C0) || (g.iL(this.C0), (this.C0 = NaN));
  };
  g.M.nG = function () {
    this.stop();
    g.ud.prototype.nG.call(this);
  };
  g.M.jA = function () {
    this.C0 = NaN;
    this.K = g.Ak(Yt(this.X, '/pairing/get_screen'), {
      method: 'POST',
      postParams: { pairing_code: this.S },
      timeout: 5e3,
      onSuccess: (0, g.fR)(this.V8, this),
      onError: (0, g.fR)(this.JX, this),
      onTimeout: (0, g.fR)(this.S0, this),
    });
  };
  g.M.V8 = function (Y, u) {
    this.K = null;
    Y = u.screen || {};
    Y.dialId = this.G;
    Y.name = this.W;
    u = -1;
    this.J &&
      Y.shortLivedLoungeToken &&
      Y.shortLivedLoungeToken.value &&
      Y.shortLivedLoungeToken.refreshIntervalMs &&
      ((Y.screenIdType = 'shortLived'),
      (Y.loungeToken = Y.shortLivedLoungeToken.value),
      (u = Y.shortLivedLoungeToken.refreshIntervalMs));
    this.publish('pairingComplete', new C8(Y), u);
  };
  g.M.JX = function (Y) {
    this.K = null;
    Y.status && Y.status == 404
      ? this.j >= oC$.length
        ? this.publish('pairingFailed', Error('DIAL polling timed out'))
        : ((Y = oC$[this.j]), (this.C0 = g.QS((0, g.fR)(this.jA, this), Y)), this.j++)
      : this.publish('pairingFailed', Error('Server error ' + Y.status));
  };
  g.M.S0 = function () {
    this.K = null;
    this.publish('pairingFailed', Error('Server not responding'));
  };
  var oC$ = [2e3, 2e3, 1e3, 1e3, 1e3, 2e3, 2e3, 5e3, 5e3, 1e4];
  g.T$(Ce, Ps);
  g.M = Ce.prototype;
  g.M.start = function () {
    SQ(this) && this.publish('screenChange');
    !g.ck('yt-remote-lounge-token-expiration') && RN$(this);
    g.iL(this.K);
    this.K = g.QS((0, g.fR)(this.start, this), 1e4);
  };
  g.M.add = function (Y, u) {
    SQ(this);
    BoR(this, Y);
    fe(this, !1);
    this.publish('screenChange');
    u(Y);
    Y.token || RN$(this);
  };
  g.M.remove = function (Y, u) {
    var n = SQ(this);
    cDq(this, Y) && (fe(this, !1), (n = !0));
    u(Y);
    n && this.publish('screenChange');
  };
  g.M.Ah = function (Y, u, n, U) {
    var k = SQ(this),
      m = this.get(Y.id);
    m
      ? (m.name != u && ((m.name = u), fe(this, !1), (k = !0)), n(Y))
      : U(Error('no such local screen.'));
    k && this.publish('screenChange');
  };
  g.M.nG = function () {
    g.iL(this.K);
    Ce.PM.nG.call(this);
  };
  g.M.O9 = function (Y) {
    SQ(this);
    var u = this.screens.length;
    Y = (Y && Y.screens) || [];
    for (var n = Y.length, U = 0; U < n; ++U) {
      var k = Y[U],
        m = this.get(k.screenId);
      m && ((m.token = k.loungeToken), --u);
    }
    fe(this, !u);
    u && ne(this.W, 'Missed ' + u + ' lounge tokens.');
  };
  g.M.L8 = function (Y) {
    ne(this.W, 'Requesting lounge tokens failed: ' + Y);
  };
  g.d(x3$, g.ud);
  g.M = x3$.prototype;
  g.M.start = function () {
    var Y = parseInt(g.ck('yt-remote-fast-check-period') || '0', 10);
    (this.G = g.iQ() - 144e5 < Y ? 0 : Y)
      ? Q5(this)
      : ((this.G = g.iQ() + 3e5), g.oU('yt-remote-fast-check-period', this.G), this.mA());
  };
  g.M.isEmpty = function () {
    return g.i4(this.K);
  };
  g.M.update = function () {
    D3J('Updating availability on schedule.');
    var Y = this.W(),
      u = g.YP(
        this.K,
        function (n, U) {
          return n && !!NC(Y, U);
        },
        this
      );
    wN$(this, u);
  };
  g.M.nG = function () {
    g.iL(this.X);
    this.X = NaN;
    this.j && (this.j.abort(), (this.j = null));
    g.ud.prototype.nG.call(this);
  };
  g.M.mA = function () {
    g.iL(this.X);
    this.X = NaN;
    this.j && this.j.abort();
    var Y = WKq(this);
    if (kqX(Y)) {
      var u = Yt(this.J, '/pairing/get_screen_availability');
      this.j = this.J.sendRequest(
        'POST',
        u,
        { lounge_token: g.C3(Y).join(',') },
        (0, g.fR)(this.mRg, this, Y),
        (0, g.fR)(this.PDF, this)
      );
    } else (wN$(this, {}), Q5(this));
  };
  g.M.mRg = function (Y, u) {
    this.j = null;
    var n = g.C3(WKq(this));
    if (g.Oq(n, g.C3(Y))) {
      u = u.screens || [];
      n = {};
      for (var U = u.length, k = 0; k < U; ++k) n[Y[u[k].loungeToken]] = u[k].status == 'online';
      wN$(this, n);
      Q5(this);
    } else (this.nk('Changing Screen set during request.'), this.mA());
  };
  g.M.PDF = function (Y) {
    this.nk('Screen availability failed: ' + Y);
    this.j = null;
    Q5(this);
  };
  g.M.nk = function (Y) {
    ne('OnlineScreenService', Y);
  };
  g.T$(Nh, Ps);
  g.M = Nh.prototype;
  g.M.start = function () {
    this.j.start();
    this.K.start();
    this.screens.length &&
      (this.publish('screenChange'), this.K.isEmpty() || this.publish('onlineScreenChange'));
  };
  g.M.add = function (Y, u, n) {
    this.j.add(Y, u, n);
  };
  g.M.remove = function (Y, u, n) {
    this.j.remove(Y, u, n);
    this.K.update();
  };
  g.M.Ah = function (Y, u, n, U) {
    this.j.contains(Y)
      ? this.j.Ah(Y, u, n, U)
      : ((Y = 'Updating name of unknown screen: ' + Y.name), ne(this.W, Y), U(Error(Y)));
  };
  g.M.XS = function (Y) {
    return Y
      ? this.screens
      : g.vu(
          this.screens,
          g.BV(
            this.X,
            function (u) {
              return !this.contains(u);
            },
            this
          )
        );
  };
  g.M.EB = function () {
    return g.BV(
      this.XS(!0),
      function (Y) {
        return !!this.K.K[Y.id];
      },
      this
    );
  };
  g.M.dQ = function (Y, u, n, U, k, m) {
    var X = this;
    this.info('getDialScreenByPairingCode ' + Y + ' / ' + u);
    var S = new vH$(this.G, Y, u, n, U);
    S.subscribe('pairingComplete', function (C, f) {
      g.nc(S);
      k(ii(X, C), f);
    });
    S.subscribe('pairingFailed', function (C) {
      g.nc(S);
      m(C);
    });
    S.start();
    return (0, g.fR)(S.stop, S);
  };
  g.M.Cv = function (Y, u, n, U) {
    g.Ak(Yt(this.G, '/pairing/get_screen'), {
      method: 'POST',
      postParams: { pairing_code: Y },
      timeout: 5e3,
      onSuccess: (0, g.fR)(function (k, m) {
        k = new C8(m.screen || {});
        if (!k.name || zN$(this, k.name)) {
          a: {
            m = k.name;
            for (var X = 2, S = u(m, X); zN$(this, S); ) {
              X++;
              if (X > 20) break a;
              S = u(m, X);
            }
            m = S;
          }
          k.name = m;
        }
        n(ii(this, k));
      }, this),
      onError: (0, g.fR)(function (k) {
        U(Error('pairing request failed: ' + k.status));
      }, this),
      onTimeout: (0, g.fR)(function () {
        U(Error('pairing request timed out.'));
      }, this),
    });
  };
  g.M.nG = function () {
    g.nc(this.j);
    g.nc(this.K);
    Nh.PM.nG.call(this);
  };
  g.M.C8 = function () {
    EHG(this);
    this.publish('screenChange');
    this.K.update();
  };
  Nh.prototype.dispose = Nh.prototype.dispose;
  g.T$(ZQ, g.ud);
  g.M = ZQ.prototype;
  g.M.gO = function (Y) {
    this.gg() ||
      (Y && (r1(this, '' + Y), this.publish('sessionFailed')),
      (this.K = null),
      this.publish('sessionScreen', null));
  };
  g.M.info = function (Y) {
    ne(this.rg, Y);
  };
  g.M.cO = function () {
    return null;
  };
  g.M.Fm = function (Y) {
    var u = this.j;
    Y
      ? ((u.displayStatus = new chrome.cast.ReceiverDisplayStatus(Y, [])),
        (u.displayStatus.showStop = !0))
      : (u.displayStatus = null);
    chrome.cast.setReceiverDisplayStatus(
      u,
      (0, g.fR)(function () {
        this.info('Updated receiver status for ' + u.friendlyName + ': ' + Y);
      }, this),
      (0, g.fR)(function () {
        r1(this, 'Failed to update receiver status for: ' + u.friendlyName);
      }, this)
    );
  };
  g.M.nG = function () {
    this.Fm('');
    ZQ.PM.nG.call(this);
  };
  g.d(Mh, ZQ);
  g.M = Mh.prototype;
  g.M.LP = function (Y) {
    if (this.X) {
      if (this.X == Y) return;
      r1(this, 'Overriding cast session with new session object');
      nk$(this);
      this.jG = !1;
      this.N = 'unknown';
      this.X.removeUpdateListener(this.oV);
      this.X.removeMessageListener('urn:x-cast:com.google.youtube.mdx', this.DW);
    }
    this.X = Y;
    this.X.addUpdateListener(this.oV);
    this.X.addMessageListener('urn:x-cast:com.google.youtube.mdx', this.DW);
    q0$(this, 'getMdxSessionStatus');
  };
  g.M.hg = function (Y) {
    this.info('launchWithParams no-op for Cast: ' + g.zE(Y));
  };
  g.M.stop = function () {
    this.X
      ? this.X.stop(
          (0, g.fR)(function () {
            this.gO();
          }, this),
          (0, g.fR)(function () {
            this.gO(Error('Failed to stop receiver app.'));
          }, this)
        )
      : this.gO(Error('Stopping cast device without session.'));
  };
  g.M.Fm = function () {};
  g.M.nG = function () {
    this.info('disposeInternal');
    nk$(this);
    this.X &&
      (this.X.removeUpdateListener(this.oV),
      this.X.removeMessageListener('urn:x-cast:com.google.youtube.mdx', this.DW));
    this.X = null;
    ZQ.prototype.nG.call(this);
  };
  g.M.WI2 = function (Y, u) {
    if (!this.gg())
      if (u)
        if (((u = U1(u)), g.XG(u)))
          switch (
            ((Y = '' + u.type),
            (u = u.data || {}),
            this.info('onYoutubeMessage_: ' + Y + ' ' + g.zE(u)),
            Y)
          ) {
            case 'mdxSessionStatus':
              Ozy(this, u);
              break;
            case 'loungeToken':
              aXL(this, u);
              break;
            default:
              r1(this, 'Unknown youtube message: ' + Y);
          }
        else r1(this, 'Unable to parse message.');
      else r1(this, 'No data in message.');
  };
  g.M.X8 = function (Y, u, n, U) {
    g.iL(this.Z);
    this.Z = 0;
    IXJ(
      this.G,
      this.j.label,
      Y,
      this.j.friendlyName,
      (0, g.fR)(function (k) {
        k
          ? u(k)
          : U >= 0
            ? (r1(this, 'Screen ' + Y + ' appears to be offline. ' + U + ' retries left.'),
              (this.Z = g.QS((0, g.fR)(this.X8, this, Y, u, n, U - 1), 300)))
            : n(Error('Unable to fetch screen.'));
      }, this),
      n
    );
  };
  g.M.cO = function () {
    return this.X;
  };
  g.M.lj = function (Y) {
    this.gg() || Y || (r1(this, 'Cast session died.'), this.gO());
  };
  g.d(sI, ZQ);
  g.M = sI.prototype;
  g.M.LP = function (Y) {
    this.X = Y;
    this.X.addUpdateListener(this.MF);
  };
  g.M.hg = function (Y) {
    this.Fk = Y;
    this.KG();
  };
  g.M.stop = function () {
    f8L(this);
    this.X
      ? this.X.stop(
          (0, g.fR)(this.gO, this, null),
          (0, g.fR)(this.gO, this, 'Failed to stop DIAL device.')
        )
      : this.gO();
  };
  g.M.nG = function () {
    f8L(this);
    this.X && this.X.removeUpdateListener(this.MF);
    this.X = null;
    ZQ.prototype.nG.call(this);
  };
  g.M.ij = function (Y) {
    this.gg() ||
      Y ||
      (r1(this, 'DIAL session died.'), this.J(), (this.J = function () {}), this.gO());
  };
  g.d(AV, ZQ);
  AV.prototype.stop = function () {
    this.gO();
  };
  AV.prototype.LP = function () {};
  AV.prototype.hg = function () {
    g.iL(this.X);
    this.X = NaN;
    var Y = NC(this.G.XS(), this.j.label);
    Y ? TM(this, Y) : this.gO(Error('No such screen'));
  };
  AV.prototype.nG = function () {
    g.iL(this.X);
    this.X = NaN;
    ZQ.prototype.nG.call(this);
  };
  g.d(jQ, g.ud);
  g.M = jQ.prototype;
  g.M.init = function (Y, u) {
    chrome.cast.timeout.requestSession = 3e4;
    var n = new chrome.cast.SessionRequest(this.Z, [chrome.cast.Capability.AUDIO_OUT]);
    g.rL('desktop_enable_cast_connect') && (n.androidReceiverCompatible = !0);
    this.N || (n.dialRequest = new chrome.cast.DialRequest('YouTube'));
    var U = chrome.cast.AutoJoinPolicy.TAB_AND_ORIGIN_SCOPED;
    Y =
      Y || this.W
        ? chrome.cast.DefaultActionPolicy.CAST_THIS_TAB
        : chrome.cast.DefaultActionPolicy.CREATE_SESSION;
    var k = (0, g.fR)(this.SDq, this);
    n = new chrome.cast.ApiConfig(n, (0, g.fR)(this.QV, this), k, U, Y);
    n.customDialLaunchCallback = (0, g.fR)(this.aWg, this);
    chrome.cast.initialize(
      n,
      (0, g.fR)(function () {
        this.gg() ||
          (chrome.cast.addReceiverActionListener(this.J),
          KKR(),
          this.j.subscribe('onlineScreenChange', (0, g.fR)(this.wQ, this)),
          (this.X = iAq(this)),
          chrome.cast.setCustomReceivers(
            this.X,
            function () {},
            (0, g.fR)(function (m) {
              this.nk('Failed to set initial custom receivers: ' + g.zE(m));
            }, this)
          ),
          this.publish('yt-remote-cast2-availability-change', pe(this)),
          u(!0));
      }, this),
      (0, g.fR)(function (m) {
        this.nk('Failed to initialize API: ' + g.zE(m));
        u(!1);
      }, this)
    );
  };
  g.M.crk = function (Y, u) {
    Ke('Setting connected screen ID: ' + Y + ' -> ' + u);
    if (this.K) {
      var n = this.K.K;
      if (!Y || (n && n.id != Y))
        (Ke('Unsetting old screen status: ' + this.K.j.friendlyName), Le(this, null));
    }
    if (Y && u) {
      if (!this.K) {
        Y = NC(this.j.XS(), Y);
        if (!Y) {
          Ke('setConnectedScreenStatus: Unknown screen.');
          return;
        }
        if (Y.idType == 'shortLived') {
          Ke('setConnectedScreenStatus: Screen with id type to be short lived.');
          return;
        }
        n = QB$(this, Y);
        n ||
          (Ke('setConnectedScreenStatus: Connected receiver not custom...'),
          (n = new chrome.cast.Receiver(Y.uuid ? Y.uuid : Y.id, Y.name)),
          (n.receiverType = chrome.cast.ReceiverType.CUSTOM),
          this.X.push(n),
          chrome.cast.setCustomReceivers(
            this.X,
            function () {},
            (0, g.fR)(function (U) {
              this.nk('Failed to set initial custom receivers: ' + g.zE(U));
            }, this)
          ));
        Ke('setConnectedScreenStatus: new active receiver: ' + n.friendlyName);
        Le(this, new AV(this.j, n), !0);
      }
      this.K.Fm(u);
    } else Ke('setConnectedScreenStatus: no screen.');
  };
  g.M.TLc = function (Y) {
    this.gg()
      ? this.nk('Setting connection data on disposed cast v2')
      : this.K
        ? this.K.hg(Y)
        : this.nk('Setting connection data without a session');
  };
  g.M.BE = function () {
    this.gg()
      ? this.nk('Stopping session on disposed cast v2')
      : this.K
        ? (this.K.stop(), Le(this, null))
        : Ke('Stopping non-existing session');
  };
  g.M.requestSession = function () {
    chrome.cast.requestSession((0, g.fR)(this.QV, this), (0, g.fR)(this.tuW, this));
  };
  g.M.nG = function () {
    this.j.unsubscribe('onlineScreenChange', (0, g.fR)(this.wQ, this));
    window.chrome && chrome.cast && chrome.cast.removeReceiverActionListener(this.J);
    var Y = GlR,
      u = g.nR('yt.mdx.remote.debug.handlers_');
    g.pR(u || [], Y);
    g.nc(this.K);
    g.ud.prototype.nG.call(this);
  };
  g.M.nk = function (Y) {
    ne('Controller', Y);
  };
  g.M.ea = function (Y, u) {
    this.K == Y && (u || Le(this, null), this.publish('yt-remote-cast2-session-change', u));
  };
  g.M.MuV = function (Y, u) {
    if (!this.gg())
      if (Y)
        switch (
          ((Y.friendlyName = chrome.cast.unescape(Y.friendlyName)),
          Ke('onReceiverAction_ ' + Y.label + ' / ' + Y.friendlyName + '-- ' + u),
          u)
        ) {
          case chrome.cast.ReceiverAction.CAST:
            if (this.K)
              if (this.K.j.label != Y.label)
                (Ke('onReceiverAction_: Stopping active receiver: ' + this.K.j.friendlyName),
                  this.K.stop());
              else {
                Ke('onReceiverAction_: Casting to active receiver.');
                this.K.K && this.publish('yt-remote-cast2-session-change', this.K.K);
                break;
              }
            switch (Y.receiverType) {
              case chrome.cast.ReceiverType.CUSTOM:
                Le(this, new AV(this.j, Y));
                break;
              case chrome.cast.ReceiverType.DIAL:
                Le(this, new sI(this.j, Y, this.G, this.config_));
                break;
              case chrome.cast.ReceiverType.CAST:
                Le(this, new Mh(this.j, Y, this.config_));
                break;
              default:
                this.nk('Unknown receiver type: ' + Y.receiverType);
            }
            break;
          case chrome.cast.ReceiverAction.STOP:
            this.K && this.K.j.label == Y.label
              ? this.K.stop()
              : this.nk('Stopping receiver w/o session: ' + Y.friendlyName);
        }
      else this.nk('onReceiverAction_ called without receiver.');
  };
  g.M.aWg = function (Y) {
    if (this.gg()) return Promise.reject(Error('disposed'));
    var u = Y.receiver;
    u.receiverType != chrome.cast.ReceiverType.DIAL &&
      (this.nk('Not DIAL receiver: ' + u.friendlyName),
      (u.receiverType = chrome.cast.ReceiverType.DIAL));
    var n = this.K ? this.K.j : null;
    if (!n || n.label != u.label)
      return (
        this.nk('Receiving DIAL launch request for non-clicked DIAL receiver: ' + u.friendlyName),
        Promise.reject(Error('illegal DIAL launch'))
      );
    if (n && n.label == u.label && n.receiverType != chrome.cast.ReceiverType.DIAL) {
      if (this.K.K)
        return (
          Ke('Reselecting dial screen.'),
          this.publish('yt-remote-cast2-session-change', this.K.K),
          Promise.resolve(new chrome.cast.DialLaunchResponse(!1))
        );
      this.nk('Changing CAST intent from "' + n.receiverType + '" to "dial" for ' + u.friendlyName);
      Le(this, new sI(this.j, u, this.G, this.config_));
    }
    u = this.K;
    u.Z = Y;
    u.Z.appState == chrome.cast.DialAppState.RUNNING
      ? ((Y = u.Z.extraData || {}),
        (n = Y.screenId || null),
        d1(u) && Y.loungeToken
          ? Y.loungeTokenRefreshIntervalMs
            ? (Y = PaQ(
                u,
                {
                  name: u.j.friendlyName,
                  screenId: Y.screenId,
                  loungeToken: Y.loungeToken,
                  dialId: u.Z.receiver.label,
                  screenIdType: 'shortLived',
                },
                Y.loungeTokenRefreshIntervalMs
              ))
            : (g.VM(
                Error(
                  'No loungeTokenRefreshIntervalMs presents in additionalData: ' +
                    JSON.stringify(Y) +
                    '.'
                )
              ),
              (Y = SLC(u, n)))
          : (Y = SLC(u, n)))
      : (Y = m9Q(u));
    return Y;
  };
  g.M.QV = function (Y) {
    var u = this;
    if (!this.gg() && !this.W) {
      Ke('New cast session ID: ' + Y.sessionId);
      var n = Y.receiver;
      if (n.receiverType != chrome.cast.ReceiverType.CUSTOM) {
        if (!this.K)
          if (n.receiverType == chrome.cast.ReceiverType.CAST)
            (Ke('Got resumed cast session before resumed mdx connection.'),
              (n.friendlyName = chrome.cast.unescape(n.friendlyName)),
              Le(this, new Mh(this.j, n, this.config_), !0));
          else {
            this.nk('Got non-cast session without previous mdx receiver event, or mdx resume.');
            return;
          }
        var U = this.K.j,
          k = NC(this.j.XS(), U.label);
        k &&
          f8(k, n.label) &&
          U.receiverType != chrome.cast.ReceiverType.CAST &&
          n.receiverType == chrome.cast.ReceiverType.CAST &&
          (Ke('onSessionEstablished_: manual to cast session change ' + n.friendlyName),
          g.nc(this.K),
          (this.K = new Mh(this.j, n, this.config_)),
          this.K.subscribe('sessionScreen', (0, g.fR)(this.ea, this, this.K)),
          this.K.subscribe('sessionFailed', function () {
            return NlG(u, u.K);
          }),
          this.K.hg(null));
        this.K.LP(Y);
      }
    }
  };
  g.M.kB = function () {
    return this.K ? this.K.cO() : null;
  };
  g.M.tuW = function (Y) {
    this.gg() ||
      (this.nk('Failed to estabilish a session: ' + g.zE(Y)),
      Y.code != chrome.cast.ErrorCode.CANCEL && Le(this, null),
      this.publish('yt-remote-cast2-session-failed'));
  };
  g.M.SDq = function (Y) {
    Ke('Receiver availability updated: ' + Y);
    if (!this.gg()) {
      var u = pe(this);
      this.S = Y == chrome.cast.ReceiverAvailability.AVAILABLE;
      pe(this) != u && this.publish('yt-remote-cast2-availability-change', pe(this));
    }
  };
  g.M.wQ = function () {
    this.gg() ||
      ((this.X = iAq(this)),
      Ke('Updating custom receivers: ' + g.zE(this.X)),
      chrome.cast.setCustomReceivers(
        this.X,
        function () {},
        (0, g.fR)(function () {
          this.nk('Failed to set custom receivers.');
        }, this)
      ),
      this.publish('yt-remote-cast2-availability-change', pe(this)));
  };
  jQ.prototype.setLaunchParams = jQ.prototype.TLc;
  jQ.prototype.setConnectedScreenStatus = jQ.prototype.crk;
  jQ.prototype.stopSession = jQ.prototype.BE;
  jQ.prototype.getCastSession = jQ.prototype.kB;
  jQ.prototype.requestSession = jQ.prototype.requestSession;
  jQ.prototype.init = jQ.prototype.init;
  jQ.prototype.dispose = jQ.prototype.dispose;
  var clC = g.rG(['https://www.gstatic.com/cv/js/sender/v1/cast_sender.js']),
    Kky = [],
    GSq = g.Y3(clC);
  g.M = DQ.prototype;
  g.M.reset = function (Y) {
    this.listId = '';
    this.index = -1;
    this.videoId = '';
    c2B(this);
    this.volume = -1;
    this.muted = !1;
    Y &&
      ((this.index = Y.index),
      (this.listId = Y.listId),
      (this.videoId = Y.videoId),
      (this.playerState = Y.playerState),
      (this.volume = Y.volume),
      (this.muted = Y.muted),
      (this.audioTrackId = Y.audioTrackId),
      (this.trackData = Y.trackData),
      (this.ZC = Y.hasPrevious),
      (this.ul = Y.hasNext),
      (this.W = Y.playerTime),
      (this.J = Y.playerTimeAt),
      (this.j = Y.seekableStart),
      (this.S = Y.seekableEnd),
      (this.X = Y.duration),
      (this.Z = Y.loadedTime),
      (this.K = Y.liveIngestionTime),
      (this.G = !isNaN(this.K)));
  };
  g.M.isPlaying = function () {
    return this.playerState == 1;
  };
  g.M.isBuffering = function () {
    return this.playerState == 3;
  };
  g.M.Jp = function (Y) {
    this.X = isNaN(Y) ? 0 : Y;
  };
  g.M.getDuration = function () {
    return this.G ? this.X + xt(this) : this.X;
  };
  g.M.clone = function () {
    return new DQ(RTG(this));
  };
  g.d(eQ, g.ud);
  g.M = eQ.prototype;
  g.M.getState = function () {
    return this.X;
  };
  g.M.nf = function () {
    return this.G.getReconnectTimeout();
  };
  g.M.Jc = function () {
    this.G.reconnect();
  };
  g.M.play = function () {
    Ig(this)
      ? (this.K ? this.K.play(null, g.lN, Hs(this, 'play')) : EI(this, 'play'),
        l8R(this, 1, hV(bi(this))),
        this.publish('remotePlayerChange'))
      : zM(this, this.play);
  };
  g.M.pause = function () {
    Ig(this)
      ? (this.K ? this.K.pause(null, g.lN, Hs(this, 'pause')) : EI(this, 'pause'),
        l8R(this, 2, hV(bi(this))),
        this.publish('remotePlayerChange'))
      : zM(this, this.pause);
  };
  g.M.seekTo = function (Y) {
    if (Ig(this)) {
      if (this.K) {
        var u = bi(this),
          n = new chrome.cast.media.SeekRequest();
        n.currentTime = Y;
        u.isPlaying() || u.isBuffering()
          ? (n.resumeState = chrome.cast.media.ResumeState.PLAYBACK_START)
          : (n.resumeState = chrome.cast.media.ResumeState.PLAYBACK_PAUSE);
        this.K.seek(n, g.lN, Hs(this, 'seekTo', { newTime: Y }));
      } else EI(this, 'seekTo', { newTime: Y });
      l8R(this, 3, Y);
      this.publish('remotePlayerChange');
    } else zM(this, g.QC(this.seekTo, Y));
  };
  g.M.stop = function () {
    if (Ig(this)) {
      this.K ? this.K.stop(null, g.lN, Hs(this, 'stopVideo')) : EI(this, 'stopVideo');
      var Y = bi(this);
      Y.index = -1;
      Y.videoId = '';
      c2B(Y);
      g1(this, Y);
      this.publish('remotePlayerChange');
    } else zM(this, this.stop);
  };
  g.M.setVolume = function (Y, u) {
    if (Ig(this)) {
      var n = bi(this);
      if (this.j) {
        if (n.volume != Y) {
          var U = Math.round(Y) / 100;
          this.j.setReceiverVolumeLevel(
            U,
            (0, g.fR)(function () {
              UI('set receiver volume: ' + U);
            }, this),
            (0, g.fR)(function () {
              this.nk('failed to set receiver volume.');
            }, this)
          );
        }
        n.muted != u &&
          this.j.setReceiverMuted(
            u,
            (0, g.fR)(function () {
              UI('set receiver muted: ' + u);
            }, this),
            (0, g.fR)(function () {
              this.nk('failed to set receiver muted.');
            }, this)
          );
      } else {
        var k = { volume: Y, muted: u };
        n.volume != -1 && (k.delta = Y - n.volume);
        EI(this, 'setVolume', k);
      }
      n.muted = u;
      n.volume = Y;
      g1(this, n);
    } else zM(this, g.QC(this.setVolume, Y, u));
  };
  g.M.pS = function (Y, u) {
    if (Ig(this)) {
      var n = bi(this);
      Y = { videoId: Y };
      u &&
        ((n.trackData = {
          trackName: u.name,
          languageCode: u.languageCode,
          sourceLanguageCode: u.translationLanguage ? u.translationLanguage.languageCode : '',
          languageName: u.languageName,
          kind: u.kind,
        }),
        (Y.style = g.zE(u.style)),
        g.sF(Y, n.trackData));
      EI(this, 'setSubtitlesTrack', Y);
      g1(this, n);
    } else zM(this, g.QC(this.pS, Y, u));
  };
  g.M.setAudioTrack = function (Y, u) {
    Ig(this)
      ? ((u = u.getLanguageInfo().getId()),
        EI(this, 'setAudioTrack', { videoId: Y, audioTrackId: u }),
        (Y = bi(this)),
        (Y.audioTrackId = u),
        g1(this, Y))
      : zM(this, g.QC(this.setAudioTrack, Y, u));
  };
  g.M.playVideo = function (Y, u, n, U, k, m, X) {
    U = U === void 0 ? null : U;
    k = k === void 0 ? null : k;
    m = m === void 0 ? null : m;
    X = X === void 0 ? null : X;
    var S = bi(this),
      C = { videoId: Y };
    n !== void 0 && (C.currentIndex = n);
    w1(S, Y, n || 0);
    u !== void 0 && (li(S, u), (C.currentTime = u));
    U && (C.listId = U);
    k && (C.playerParams = k);
    m && (C.clickTrackingParams = m);
    X && (C.locationInfo = g.zE(X));
    EI(this, 'setPlaylist', C);
    U || g1(this, S);
  };
  g.M.Xi = function (Y, u) {
    if (Ig(this)) {
      if (Y && u) {
        var n = bi(this);
        w1(n, Y, u);
        g1(this, n);
      }
      EI(this, 'previous');
    } else zM(this, g.QC(this.Xi, Y, u));
  };
  g.M.nextVideo = function (Y, u) {
    if (Ig(this)) {
      if (Y && u) {
        var n = bi(this);
        w1(n, Y, u);
        g1(this, n);
      }
      EI(this, 'next');
    } else zM(this, g.QC(this.nextVideo, Y, u));
  };
  g.M.hC = function () {
    if (Ig(this)) {
      EI(this, 'clearPlaylist');
      var Y = bi(this);
      Y.reset();
      g1(this, Y);
      this.publish('remotePlayerChange');
    } else zM(this, this.hC);
  };
  g.M.O4 = function () {
    Ig(this) ? EI(this, 'dismissAutoplay') : zM(this, this.O4);
  };
  g.M.dispose = function () {
    if (this.X != 3) {
      var Y = this.X;
      this.X = 3;
      this.publish('proxyStateChange', Y, this.X);
    }
    g.ud.prototype.dispose.call(this);
  };
  g.M.nG = function () {
    x9C(this);
    this.G = null;
    this.J.clear();
    Ws(this, null);
    g.ud.prototype.nG.call(this);
  };
  g.M.ge = function (Y) {
    if ((Y != this.X || Y == 2) && this.X != 3 && Y != 0) {
      var u = this.X;
      this.X = Y;
      this.publish('proxyStateChange', u, Y);
      if (Y == 1)
        for (; !this.J.isEmpty(); )
          ((u = Y = this.J),
            u.K.length === 0 && ((u.K = u.j), u.K.reverse(), (u.j = [])),
            Y.K.pop().apply(this));
      else Y == 3 && this.dispose();
    }
  };
  g.M.Wok = function (Y, u) {
    this.publish(Y, u);
  };
  g.M.wzg = function (Y) {
    if (!Y) (this.Mj(null), Ws(this, null));
    else if (this.j.receiver.volume) {
      Y = this.j.receiver.volume;
      var u = bi(this),
        n = Math.round(100 * Y.level || 0);
      if (u.volume != n || u.muted != Y.muted)
        (UI('Cast volume update: ' + Y.level + (Y.muted ? ' muted' : '')),
          (u.volume = n),
          (u.muted = !!Y.muted),
          g1(this, u));
    }
  };
  g.M.Mj = function (Y) {
    UI('Cast media: ' + !!Y);
    this.K && this.K.removeUpdateListener(this.Z);
    if ((this.K = Y))
      (this.K.addUpdateListener(this.Z), hTg(this), this.publish('remotePlayerChange'));
  };
  g.M.cJz = function (Y) {
    Y ? (hTg(this), this.publish('remotePlayerChange')) : this.Mj(null);
  };
  g.M.RL = function () {
    EI(this, 'sendDebugCommand', { debugCommand: 'stats4nerds ' });
  };
  g.M.z22 = function () {
    var Y = t6L();
    Y && Ws(this, Y);
  };
  g.M.nk = function (Y) {
    ne('CP', Y);
  };
  g.d(OI, g.ud);
  g.M = OI.prototype;
  g.M.connect = function (Y, u) {
    if (u) {
      var n = u.listId,
        U = u.videoId,
        k = u.videoIds,
        m = u.playerParams,
        X = u.clickTrackingParams,
        S = u.index,
        C = { videoId: U },
        f = u.currentTime,
        Q = u.locationInfo;
      u = u.loopMode;
      f !== void 0 && (C.currentTime = f <= 5 ? 0 : f);
      m && (C.playerParams = m);
      Q && (C.locationInfo = Q);
      X && (C.clickTrackingParams = X);
      n && (C.listId = n);
      k && k.length > 0 && (C.videoIds = k.join(','));
      S !== void 0 && (C.currentIndex = S);
      this.MF && (C.loopMode = u || 'LOOP_MODE_OFF');
      n && (this.K.listId = n);
      this.K.videoId = U;
      this.K.index = S || 0;
      this.K.state = 3;
      li(this.K, f);
      this.J = 'UNSUPPORTED';
      n = this.MF ? 'setInitialState' : 'setPlaylist';
      y5('Connecting with ' + n + ' and params: ' + g.zE(C));
      this.j.connect({ method: n, params: g.zE(C) }, Y, $IX());
    } else (y5('Connecting without params'), this.j.connect({}, Y, $IX()));
    bAL(this);
  };
  g.M.KL = function (Y) {
    this.j.KL(Y);
  };
  g.M.dispose = function () {
    this.gg() ||
      (g.Y$('yt.mdx.remote.remoteClient_', null), this.publish('beforeDispose'), V5(this, 3));
    g.ud.prototype.dispose.call(this);
  };
  g.M.nG = function () {
    I8C(this);
    gkX(this);
    zTC(this);
    g.iL(this.Z);
    this.Z = NaN;
    g.iL(this.N);
    this.N = NaN;
    this.G = null;
    g.dT(this.KG);
    this.KG.length = 0;
    this.j.dispose();
    g.ud.prototype.nG.call(this);
    this.J = this.S = this.X = this.K = this.j = null;
  };
  g.M.N9 = function (Y) {
    if (!this.X || this.X.length === 0) return !1;
    for (var u = g.A(this.X), n = u.next(); !n.done; n = u.next())
      if (!n.value.capabilities.has(Y)) return !1;
    return !0;
  };
  g.M.tP = function () {
    var Y = 3;
    this.gg() || ((Y = 0), isNaN(this.GA()) ? this.j.OZ() && isNaN(this.W) && (Y = 1) : (Y = 2));
    return Y;
  };
  g.M.Rs = function (Y) {
    y5('Disconnecting with ' + Y);
    g.Y$('yt.mdx.remote.remoteClient_', null);
    I8C(this);
    this.publish('beforeDisconnect', Y);
    Y == 1 && Tx();
    this.j.disconnect(Y);
    this.dispose();
  };
  g.M.zJ = function () {
    var Y = this.K;
    this.G && ((Y = this.K.clone()), w1(Y, this.G, Y.index));
    return RTG(Y);
  };
  g.M.P8c = function (Y) {
    var u = this,
      n = new DQ(Y);
    n.videoId &&
      n.videoId != this.K.videoId &&
      ((this.G = n.videoId),
      g.iL(this.Z),
      (this.Z = g.QS(function () {
        if (u.G) {
          var k = u.G;
          u.G = null;
          u.K.videoId != k && Fm(u, 'getNowPlaying');
        }
      }, 5e3)));
    var U = [];
    (this.K.listId == n.listId && this.K.videoId == n.videoId && this.K.index == n.index) ||
      U.push('remoteQueueChange');
    (this.K.playerState == n.playerState &&
      this.K.volume == n.volume &&
      this.K.muted == n.muted &&
      hV(this.K) == hV(n) &&
      g.zE(this.K.trackData) == g.zE(n.trackData)) ||
      U.push('remotePlayerChange');
    this.K.reset(Y);
    g.Jy(
      U,
      function (k) {
        this.publish(k);
      },
      this
    );
  };
  g.M.f9 = function () {
    var Y = this.j.getDeviceId(),
      u = g.G$(this.X, function (n) {
        return n.type == 'REMOTE_CONTROL' && n.id != Y;
      });
    return u ? u.id : '';
  };
  g.M.GA = function () {
    return this.j.nf();
  };
  g.M.gx = function () {
    return this.J || 'UNSUPPORTED';
  };
  g.M.MK = function () {
    return this.S || '';
  };
  g.M.Q8 = function () {
    !isNaN(this.GA()) && this.j.Jc();
  };
  g.M.ZpG = function (Y, u) {
    Fm(this, Y, u);
    HAR(this);
  };
  g.M.zv = function () {
    var Y = g.Dz('SAPISID', '') || g.Dz('__Secure-1PAPISID') || '',
      u = g.Dz('__Secure-3PAPISID', '') || '';
    if (!Y && !u) return '';
    Y = g.oE(g.Bi(Y), 2);
    u = g.oE(g.Bi(u), 2);
    return g.oE(g.Bi(',' + Y + ',' + u), 2);
  };
  OI.prototype.subscribe = OI.prototype.subscribe;
  OI.prototype.unsubscribeByKey = OI.prototype.eh;
  OI.prototype.getProxyState = OI.prototype.tP;
  OI.prototype.disconnect = OI.prototype.Rs;
  OI.prototype.getPlayerContextData = OI.prototype.zJ;
  OI.prototype.setPlayerContextData = OI.prototype.P8c;
  OI.prototype.getOtherConnectedRemoteId = OI.prototype.f9;
  OI.prototype.getReconnectTimeout = OI.prototype.GA;
  OI.prototype.getAutoplayMode = OI.prototype.gx;
  OI.prototype.getAutoplayVideoId = OI.prototype.MK;
  OI.prototype.reconnect = OI.prototype.Q8;
  OI.prototype.sendMessage = OI.prototype.ZpG;
  OI.prototype.getXsrfToken = OI.prototype.zv;
  OI.prototype.isCapabilitySupportedOnConnectedDevices = OI.prototype.N9;
  g.d(UnG, Ps);
  g.M = UnG.prototype;
  g.M.XS = function (Y) {
    return this.o_.$_gs(Y);
  };
  g.M.contains = function (Y) {
    return !!this.o_.$_c(Y);
  };
  g.M.get = function (Y) {
    return this.o_.$_g(Y);
  };
  g.M.start = function () {
    this.o_.$_st();
  };
  g.M.add = function (Y, u, n) {
    this.o_.$_a(Y, u, n);
  };
  g.M.remove = function (Y, u, n) {
    this.o_.$_r(Y, u, n);
  };
  g.M.Ah = function (Y, u, n, U) {
    this.o_.$_un(Y, u, n, U);
  };
  g.M.nG = function () {
    for (var Y = this.K.length, u = 0; u < Y; ++u) this.o_.$_ubk(this.K[u]);
    this.K.length = 0;
    this.o_ = null;
    Ps.prototype.nG.call(this);
  };
  g.M.ZS = function () {
    this.publish('screenChange');
  };
  g.M.lFF = function () {
    this.publish('onlineScreenChange');
  };
  Nh.prototype.$_st = Nh.prototype.start;
  Nh.prototype.$_gspc = Nh.prototype.Cv;
  Nh.prototype.$_gsppc = Nh.prototype.dQ;
  Nh.prototype.$_c = Nh.prototype.contains;
  Nh.prototype.$_g = Nh.prototype.get;
  Nh.prototype.$_a = Nh.prototype.add;
  Nh.prototype.$_un = Nh.prototype.Ah;
  Nh.prototype.$_r = Nh.prototype.remove;
  Nh.prototype.$_gs = Nh.prototype.XS;
  Nh.prototype.$_gos = Nh.prototype.EB;
  Nh.prototype.$_s = Nh.prototype.subscribe;
  Nh.prototype.$_ubk = Nh.prototype.eh;
  var Xv = null,
    Cf = !1,
    JV = null,
    qh = null,
    ZCq = null,
    up = [];
  g.d(dng, g.e);
  g.M = dng.prototype;
  g.M.nG = function () {
    g.e.prototype.nG.call(this);
    this.j.stop();
    this.X.stop();
    this.Z.stop();
    var Y = this.YV;
    Y.unsubscribe('proxyStateChange', this.k0, this);
    Y.unsubscribe('remotePlayerChange', this.lK, this);
    Y.unsubscribe('remoteQueueChange', this.pg, this);
    Y.unsubscribe('previousNextChange', this.Sa, this);
    Y.unsubscribe('nowAutoplaying', this.Wf, this);
    Y.unsubscribe('autoplayDismissed', this.RT, this);
    this.YV = this.K = null;
  };
  g.M.G3 = function (Y) {
    var u = g.It.apply(1, arguments);
    if (this.YV.X != 2)
      if (ff(this)) {
        if (bi(this.YV).playerState != 1081 || Y !== 'control_seek')
          switch (Y) {
            case 'control_toggle_play_pause':
              bi(this.YV).isPlaying() ? this.YV.pause() : this.YV.play();
              break;
            case 'control_play':
              this.YV.play();
              break;
            case 'control_pause':
              this.YV.pause();
              break;
            case 'control_seek':
              this.S.pw(u[0], u[1]);
              break;
            case 'control_subtitles_set_track':
              Alu(this, u[0]);
              break;
            case 'control_set_audio_track':
              this.setAudioTrack(u[0]);
          }
      } else
        switch (Y) {
          case 'control_toggle_play_pause':
          case 'control_play':
          case 'control_pause':
            u = this.L.getCurrentTime();
            QG(this, u === 0 ? void 0 : u);
            break;
          case 'control_seek':
            QG(this, u[0]);
            break;
          case 'control_subtitles_set_track':
            Alu(this, u[0]);
            break;
          case 'control_set_audio_track':
            this.setAudioTrack(u[0]);
        }
  };
  g.M.EwZ = function (Y) {
    this.Z.Ga(Y);
  };
  g.M.maG = function (Y) {
    this.G3('control_subtitles_set_track', g.i4(Y) ? null : Y);
  };
  g.M.dN = function () {
    var Y = this.L.getOption('captions', 'track');
    g.i4(Y) || Alu(this, Y);
  };
  g.M.ye = function (Y) {
    this.K.ye(Y, this.L.getVideoData().lengthSeconds);
  };
  g.M.y_g = function () {
    g.i4(this.G) || jb$(this, this.G);
    this.J = !1;
  };
  g.M.k0 = function (Y, u) {
    this.X.stop();
    u === 2 && this.AB();
  };
  g.M.lK = function () {
    if (ff(this)) {
      this.j.stop();
      var Y = bi(this.YV);
      switch (Y.playerState) {
        case 1080:
        case 1081:
        case 1084:
        case 1085:
          this.K.oM = 1;
          break;
        case 1082:
        case 1083:
          this.K.oM = 0;
          break;
        default:
          this.K.oM = -1;
      }
      switch (Y.playerState) {
        case 1081:
        case 1:
          this.t_(new g.RZ(8));
          this.HT();
          break;
        case 1085:
        case 3:
          this.t_(new g.RZ(9));
          break;
        case 1083:
        case 0:
          this.t_(new g.RZ(2));
          this.S.stop();
          this.ye(this.L.getVideoData().lengthSeconds);
          break;
        case 1084:
          this.t_(new g.RZ(4));
          break;
        case 2:
          this.t_(new g.RZ(4));
          this.ye(hV(Y));
          break;
        case -1:
          this.t_(new g.RZ(64));
          break;
        case -1e3:
          this.t_(
            new g.RZ(128, {
              errorCode: 'mdx.remoteerror',
              errorMessage: 'Ta videoposnetek ni na voljo za oddaljeno predvajanje.',
              yz: 2,
            })
          );
      }
      Y = bi(this.YV).trackData;
      var u = this.G;
      (Y || u
        ? Y &&
          u &&
          Y.trackName == u.trackName &&
          Y.languageCode == u.languageCode &&
          Y.languageName == u.languageName &&
          Y.kind == u.kind
        : 1) || ((this.G = Y), jb$(this, Y));
      Y = bi(this.YV);
      Y.volume === -1 ||
        (Math.round(this.L.getVolume()) === Y.volume && this.L.isMuted() === Y.muted) ||
        this.N.isActive() ||
        this.lz();
    } else Gnq(this);
  };
  g.M.Sa = function () {
    this.L.publish('mdxpreviousnextchange');
  };
  g.M.pg = function () {
    ff(this) || Gnq(this);
  };
  g.M.Wf = function (Y) {
    isNaN(Y) || this.L.publish('mdxnowautoplaying', Y);
  };
  g.M.RT = function () {
    this.L.publish('mdxautoplaycanceled');
  };
  g.M.setAudioTrack = function (Y) {
    ff(this) && this.YV.setAudioTrack(this.L.getVideoData(1).videoId, Y);
  };
  g.M.seekTo = function (Y, u) {
    bi(this.YV).playerState === -1 ? QG(this, Y) : u && this.YV.seekTo(Y);
  };
  g.M.lz = function () {
    var Y = this;
    if (ff(this)) {
      var u = bi(this.YV);
      this.events.qR(this.KG);
      u.muted ? this.L.mute() : this.L.unMute();
      this.L.setVolume(u.volume);
      this.KG = this.events.B(this.L, 'onVolumeChange', function (n) {
        MgX(Y, n);
      });
    }
  };
  g.M.HT = function () {
    this.j.stop();
    if (!this.YV.gg()) {
      var Y = bi(this.YV);
      Y.isPlaying() && this.t_(new g.RZ(8));
      this.ye(hV(Y));
      this.j.start();
    }
  };
  g.M.AB = function () {
    this.X.stop();
    this.j.stop();
    var Y = this.YV.nf();
    this.YV.X == 2 && !isNaN(Y) && this.X.start();
  };
  g.M.t_ = function (Y) {
    this.X.stop();
    var u = this.W;
    if (!g.Wa(u, Y)) {
      var n = g.V(Y, 2);
      n !== g.V(this.W, 2) && this.L.ZX(n);
      this.W = Y;
      LCq(this.K, u, Y);
    }
  };
  g.d(KCJ, g.qa);
  g.M = KCJ.prototype;
  g.M.getCurrentTime = function () {
    return this.K.getCurrentTime();
  };
  g.M.getDuration = function () {
    return this.K.getDuration();
  };
  g.M.Ia = function () {
    return this.K.Ia();
  };
  g.M.h4 = function () {
    return this.K.h4();
  };
  g.M.u4 = function () {
    return this.K.u4();
  };
  g.M.fQ = function () {
    return this.K.fQ();
  };
  g.M.getPlayerState = function () {
    return this.K.Zk;
  };
  g.M.isAtLiveHead = function () {
    return this.K.isAtLiveHead();
  };
  g.M.pauseVideo = function () {
    this.K.gr('control_pause');
  };
  g.M.playVideo = function () {
    var Y = this;
    return g.l(function (u) {
      Y.K.gr('control_play');
      return u.return();
    });
  };
  g.M.seekTo = function (Y, u) {
    this.K.gr('control_seek', Y, !(u == null ? 0 : u.AO));
  };
  g.M.Uj = function (Y) {
    this.K.gr('control_set_audio_track', Y);
    return !0;
  };
  g.d(N6, g.H);
  N6.prototype.Su = function () {
    this.fade.show();
  };
  N6.prototype.H$ = function () {
    this.fade.hide();
  };
  N6.prototype.K = function () {
    MC('mdx-privacy-popup-cancel');
    this.H$();
  };
  N6.prototype.j = function () {
    MC('mdx-privacy-popup-confirm');
    this.H$();
  };
  g.d(ip, g.H);
  ip.prototype.onStateChange = function (Y) {
    this.Ve(Y.state);
  };
  ip.prototype.Ve = function (Y) {
    if (this.api.getPresentingPlayerType() === 3) {
      var u = { RECEIVER_NAME: this.api.getOption('remote', 'currentReceiver').name };
      Y = g.V(Y, 128)
        ? g.UR('Napaka v napravi $RECEIVER_NAME', u)
        : Y.isPlaying() || Y.isPaused()
          ? g.UR('Predvajanje v napravi $RECEIVER_NAME', u)
          : g.UR('Vzpostavljena je povezava z napravo $RECEIVER_NAME', u);
      this.updateValue('statustext', Y);
      this.fade.show();
    } else this.fade.hide();
  };
  g.d(Zc, g.gJ);
  Zc.prototype.G = function () {
    var Y = this.L.getOption('remote', 'receivers');
    Y && Y.length > 1 && !this.L.getOption('remote', 'quickCast')
      ? ((this.K6 = g.qX(Y, this.K, this)),
        this.UT(g.dA(Y, this.K)),
        (Y = this.L.getOption('remote', 'currentReceiver')),
        (Y = this.K(Y)),
        this.options[Y] && this.ww(Y),
        this.enable(!0))
      : this.enable(!1);
  };
  Zc.prototype.K = function (Y) {
    return Y.key;
  };
  Zc.prototype.zg = function (Y) {
    return Y === 'cast-selector-receiver' ? 'Predvajanje ...' : this.K6[Y].name;
  };
  Zc.prototype.mM = function (Y) {
    g.gJ.prototype.mM.call(this, Y);
    this.L.setOption('remote', 'currentReceiver', this.K6[Y]);
    this.jE.H$();
  };
  g.d(prB, g.vH);
  g.M = prB.prototype;
  g.M.create = function () {
    var Y = this.player.Y(),
      u = g.SG(Y);
    Y = {
      device: 'Desktop',
      app: 'youtube-desktop',
      loadCastApiSetupScript: Y.V('mdx_load_cast_api_bootstrap_script'),
      enableDialLoungeToken: Y.V('enable_dial_short_lived_lounge_token'),
      enableCastLoungeToken: Y.V('enable_cast_short_lived_lounge_token'),
    };
    SCB(u, Y);
    this.subscriptions.push(g.q3('yt-remote-before-disconnect', this.ZGz, this));
    this.subscriptions.push(g.q3('yt-remote-connection-change', this.CDg, this));
    this.subscriptions.push(g.q3('yt-remote-receiver-availability-change', this.iP, this));
    this.subscriptions.push(g.q3('yt-remote-auto-connect', this.VuZ, this));
    this.subscriptions.push(g.q3('yt-remote-receiver-resumed', this.JRW, this));
    this.subscriptions.push(g.q3('mdx-privacy-popup-confirm', this.akg, this));
    this.subscriptions.push(g.q3('mdx-privacy-popup-cancel', this.tbz, this));
    this.iP();
  };
  g.M.load = function () {
    this.player.cancelPlayback();
    g.vH.prototype.load.call(this);
    this.RM = new KCJ(this.player.Y(), this);
    this.player.wB(this.RM);
    this.v2 = new dng(this, this.player, this.YV);
    var Y = (Y = rl$()) ? Y.currentTime : 0;
    var u = iC$() ? new eQ(mE(), void 0) : null;
    Y == 0 && u && (Y = hV(bi(u)));
    Y !== 0 && this.ye(Y);
    LCq(this, this.Zk, this.Zk);
    this.player.D8(6);
  };
  g.M.unload = function () {
    this.player.publish('mdxautoplaycanceled');
    this.player.O8();
    this.zY = this.tG;
    g.Uo(this.v2, this.YV);
    this.YV = this.RM = this.v2 = null;
    g.vH.prototype.unload.call(this);
    this.player.D8(5);
    TV(this);
  };
  g.M.nG = function () {
    g.a9(this.subscriptions);
    g.vH.prototype.nG.call(this);
  };
  g.M.gr = function (Y) {
    var u = g.It.apply(1, arguments);
    this.loaded && this.v2.G3.apply(this.v2, [Y].concat(g.Zu(u)));
  };
  g.M.getAdState = function () {
    return this.oM;
  };
  g.M.ZC = function () {
    return this.YV ? bi(this.YV).ZC : !1;
  };
  g.M.ul = function () {
    return this.YV ? bi(this.YV).ul : !1;
  };
  g.M.ye = function (Y, u) {
    this.jd = Y || 0;
    this.player.publish('progresssync', Y, u);
    this.player.oa('onVideoProgress', Y || 0);
  };
  g.M.getCurrentTime = function () {
    return this.jd;
  };
  g.M.getDuration = function () {
    return bi(this.YV).getDuration() || 0;
  };
  g.M.Ia = function () {
    var Y = bi(this.YV);
    return Y.G ? Y.K + xt(Y) : Y.K;
  };
  g.M.h4 = function () {
    return bi(this.YV).Z;
  };
  g.M.u4 = function () {
    return vkq(bi(this.YV));
  };
  g.M.fQ = function () {
    var Y = bi(this.YV);
    return Y.j > 0 ? Y.j + xt(Y) : Y.j;
  };
  g.M.getProgressState = function () {
    var Y = bi(this.YV),
      u = this.player.getVideoData();
    return {
      airingStart: 0,
      airingEnd: 0,
      allowSeeking: Y.playerState != 1081 && this.player.wV(),
      clipEnd: u.clipEnd,
      clipStart: u.clipStart,
      current: this.getCurrentTime(),
      displayedStart: -1,
      duration: this.getDuration(),
      ingestionTime: this.Ia(),
      isAtLiveHead: this.isAtLiveHead(),
      loaded: this.h4(),
      seekableEnd: this.u4(),
      seekableStart: this.fQ(),
      offset: 0,
      viewerLivestreamJoinMediaTime: 0,
    };
  };
  g.M.isAtLiveHead = function () {
    return vkq(bi(this.YV)) - this.getCurrentTime() <= 1;
  };
  g.M.nextVideo = function () {
    this.YV && this.YV.nextVideo();
  };
  g.M.Xi = function () {
    this.YV && this.YV.Xi();
  };
  g.M.ZGz = function (Y) {
    Y === 1 && (this.gR = this.YV ? bi(this.YV) : null);
  };
  g.M.CDg = function () {
    var Y = iC$() ? new eQ(mE(), void 0) : null;
    if (Y) {
      var u = this.zY;
      this.loaded && this.unload();
      this.YV = Y;
      this.gR = null;
      u.key !== this.tG.key && ((this.zY = u), this.load());
    } else
      (g.nc(this.YV),
        (this.YV = null),
        this.loaded &&
          (this.unload(),
          (Y = this.gR) &&
            Y.videoId === this.player.getVideoData().videoId &&
            this.player.cueVideoById(Y.videoId, hV(Y))));
    this.player.publish('videodatachange', 'newdata', this.player.getVideoData(), 3);
  };
  g.M.iP = function () {
    var Y = [this.tG],
      u = Y.concat,
      n = C2J();
    cs() &&
      g.ck('yt-remote-cast-available') &&
      n.push({ key: 'cast-selector-receiver', name: 'Cast...' });
    this.K6 = u.call(Y, n);
    Y = Qbq() || this.tG;
    rQ(this, Y);
    this.player.oa('onMdxReceiversChange');
  };
  g.M.VuZ = function () {
    var Y = Qbq();
    rQ(this, Y);
  };
  g.M.JRW = function () {
    this.zY = Qbq();
  };
  g.M.akg = function () {
    this.Nj = !0;
    TV(this);
    Cf = !1;
    Xv && S5(Xv, 1);
    Xv = null;
  };
  g.M.tbz = function () {
    this.Nj = !1;
    TV(this);
    rQ(this, this.tG);
    this.zY = this.tG;
    Cf = !1;
    Xv = null;
    this.player.playVideo();
  };
  g.M.z6 = function (Y, u) {
    switch (Y) {
      case 'casting':
        return this.loaded;
      case 'receivers':
        return this.K6;
      case 'currentReceiver':
        return (
          u && (u.key === 'cast-selector-receiver' ? BlJ() : rQ(this, u)),
          this.loaded ? this.zY : this.tG
        );
      case 'quickCast':
        return this.K6.length === 2 && this.K6[1].key === 'cast-selector-receiver'
          ? (u && BlJ(), !0)
          : !1;
    }
  };
  g.M.RL = function () {
    this.YV.RL();
  };
  g.M.VO = function () {
    return !1;
  };
  g.M.getOptions = function () {
    return ['casting', 'receivers', 'currentReceiver', 'quickCast'];
  };
  g.M.isLoggedIn = function () {
    var Y, u;
    return ((Y = g.z6('PLAYER_CONFIG')) == null
      ? void 0
      : (u = Y.args) == null
        ? void 0
        : u.authuser) !== void 0
      ? !0
      : !(!g.z6('SESSION_INDEX') && !g.z6('LOGGED_IN'));
  };
  g.cH('remote', prB);
})(_yt_player);
