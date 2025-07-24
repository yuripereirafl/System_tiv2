<template>
  <div>
    <h1 style="color:var(--cor-primaria);font-family:var(--font-titulo);">Dashboard</h1>
    <div v-if="loading" style="margin:48px 0;text-align:center;font-size:20px;color:var(--cor-primaria);">
      Carregando dados do dashboard...
    </div>
    <div v-else>
      <div style="display:flex;gap:32px;margin-top:32px;justify-content:center;">
        <div style="background:var(--cor-sec1);color:var(--cor-branco);padding:24px 32px;border-radius:8px;min-width:180px;text-align:center;box-shadow:0 2px 8px rgba(20,65,121,0.08);">
          <h2 style="font-family:var(--font-titulo);font-size:22px;display:flex;align-items:center;justify-content:center;gap:8px;">
            <span>Funcionários</span>
            <span style="font-size:20px;">👤</span>
          </h2>
          <div style="font-size:32px;font-weight:bold;">{{ totalFuncionarios }}</div>
          <div style="font-size:13px;margin-top:6px;">
            <span v-if="ultimoFuncionario">Último cadastro: {{ ultimoFuncionario }}</span>
          </div>
        </div>
        <div style="background:var(--cor-sec3);color:var(--cor-primaria);padding:24px 32px;border-radius:8px;min-width:180px;text-align:center;box-shadow:0 2px 8px rgba(20,65,121,0.08);">
          <h2 style="font-family:var(--font-titulo);font-size:22px;display:flex;align-items:center;justify-content:center;gap:8px;">
            <span>Setores</span>
            <span style="font-size:20px;">🏢</span>
          </h2>
          <div style="font-size:32px;font-weight:bold;">{{ totalSetores }}</div>
        </div>
        <div style="background:var(--cor-sec2);color:var(--cor-branco);padding:24px 32px;border-radius:8px;min-width:180px;text-align:center;box-shadow:0 2px 8px rgba(20,65,121,0.08);">
          <h2 style="font-family:var(--font-titulo);font-size:22px;display:flex;align-items:center;justify-content:center;gap:8px;">
            <span>Sistemas</span>
            <span style="font-size:20px;">💻</span>
          </h2>
          <div style="font-size:32px;font-weight:bold;">{{ totalSistemas }}</div>
        </div>
      </div>
      <div style="display:flex;gap:32px;margin-top:32px;justify-content:center;">
        <div style="background:var(--cor-destaque);color:var(--cor-primaria);padding:24px 32px;border-radius:8px;min-width:180px;text-align:center;box-shadow:0 2px 8px rgba(20,65,121,0.08);">
          <h2 style="font-family:var(--font-titulo);font-size:22px;display:flex;align-items:center;justify-content:center;gap:8px;">
            <span>Grupos de E-mail</span>
            <span style="font-size:20px;">📧</span>
          </h2>
          <div style="font-size:32px;font-weight:bold;">{{ gruposEmail.length }}</div>
        </div>
        <div style="background:var(--cor-sec2);color:var(--cor-branco);padding:24px 32px;border-radius:8px;min-width:180px;text-align:center;box-shadow:0 2px 8px rgba(20,65,121,0.08);">
          <h2 style="font-family:var(--font-titulo);font-size:22px;display:flex;align-items:center;justify-content:center;gap:8px;">
            <span>Cargos</span>
            <span style="font-size:20px;">🧑‍💼</span>
          </h2>
          <div style="font-size:32px;font-weight:bold;">{{ cargos.length }}</div>
        </div>
      </div>
      <div v-if="erro" style="margin-top:32px;color:#d32f2f;font-size:16px;text-align:center;">{{ erro }}</div>
    </div>
  </div>
</template>

<script>
import { API_BASE_URL } from '../api';

export default {
  name: 'DashboardPanel',
  data() {
    return {
      totalFuncionarios: 0,
      totalSetores: 0,
      totalSistemas: 0,
      gruposEmail: [],
      setores: [],
      cargos: [],
      funcionariosInativos: null,
      ultimoFuncionario: '',
      sistemasAtivos: null,
      sistemasInativos: null,
      loading: true,
      erro: ''
    }
  },
  async mounted() {
    try {
      const funcionarios = await fetch(`${API_BASE_URL}/funcionarios/`).then(r => r.json());
      this.totalFuncionarios = funcionarios.length;
      this.cargos = [...new Set(funcionarios.map(f => f.cargo).filter(Boolean))];
      this.funcionariosAtivos = funcionarios.filter(f => f.status === 'ativo').length;
      this.funcionariosInativos = funcionarios.filter(f => f.status === 'inativo').length;
      if (funcionarios.length > 0 && funcionarios[0].created_at) {
        const ultimo = funcionarios.reduce((a, b) => new Date(a.created_at) > new Date(b.created_at) ? a : b);
        this.ultimoFuncionario = new Date(ultimo.created_at).toLocaleDateString('pt-BR');
      }
      const setores = await fetch(`${API_BASE_URL}/setores/`).then(r => r.json()).catch(() => []);
      this.totalSetores = setores.length;
      this.setores = setores;
      const sistemas = await fetch(`${API_BASE_URL}/sistemas/`).then(r => r.json());
      this.totalSistemas = sistemas.length;
      this.sistemasAtivos = sistemas.filter(s => s.status === 'ativo').length;
      this.sistemasInativos = sistemas.filter(s => s.status === 'inativo').length;
      const gruposEmail = await fetch(`${API_BASE_URL}/grupos-email/`).then(r => r.json()).catch(() => []);
      this.gruposEmail = gruposEmail;
      this.loading = false;
    } catch (e) {
      this.erro = 'Erro ao carregar dados do dashboard.';
      this.loading = false;
    }
  }
}
</script>
