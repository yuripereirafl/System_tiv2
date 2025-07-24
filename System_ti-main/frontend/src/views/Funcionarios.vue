<template>
  <div class="tabela-funcionarios">
    <div class="header header-funcionarios">
      <h2>Funcionários</h2>
      <div class="busca-adicionar">
        <input v-model="buscaFuncionario" placeholder="Buscar funcionário..." class="input-busca" />
        <button class="btn-cadastrar" @click="showForm = !showForm">
          + Adicionar Funcionário
        </button>
      </div>
    </div>
    <div class="dica-expansao">
    </div>
    <table>
      <thead>
        <tr>
          <th>Nome</th>
          <th>Sobrenome</th>
          <th>Celular</th>
          <th>E-mail</th>
          <th>Grupo E-mail</th>
          <th>Setor</th>
          <th>Cargo</th>
          <th>Sistemas</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="func in funcionariosFiltrados" :key="func.id">
          <td @click="toggleCelulaExpandida(func.id, 'nome')" 
              :class="{ expandida: isCelulaExpandida(func.id, 'nome') }"
              class="clicavel">{{ func.nome }}</td>
          <td @click="toggleCelulaExpandida(func.id, 'sobrenome')" 
              :class="{ expandida: isCelulaExpandida(func.id, 'sobrenome') }"
              class="clicavel">{{ func.sobrenome }}</td>
          <td @click="toggleCelulaExpandida(func.id, 'celular')" 
              :class="{ expandida: isCelulaExpandida(func.id, 'celular') }"
              class="clicavel">{{ func.celular }}</td>
          <td @click="toggleCelulaExpandida(func.id, 'email')" 
              :class="{ expandida: isCelulaExpandida(func.id, 'email') }"
              class="clicavel">{{ func.email }}</td>
          <td @click="toggleCelulaExpandida(func.id, 'grupos')" 
              :class="{ expandida: isCelulaExpandida(func.id, 'grupos') }"
              class="clicavel">
            <span v-if="func.grupos_email && func.grupos_email.length">
              {{ func.grupos_email.map(g => g.nome).join(', ') }}
            </span>
            <span v-else>—</span>
          </td>
          <td @click="toggleCelulaExpandida(func.id, 'setores')" 
              :class="{ expandida: isCelulaExpandida(func.id, 'setores') }"
              class="clicavel">{{ func.setores && func.setores.length ? func.setores.map(s => s.nome).join(', ') : '—' }}</td>
          <td @click="toggleCelulaExpandida(func.id, 'cargo')" 
              :class="{ expandida: isCelulaExpandida(func.id, 'cargo') }"
              class="clicavel">{{ func.cargo || '—' }}</td>
          <td @click="toggleCelulaExpandida(func.id, 'sistemas')" 
              :class="{ expandida: isCelulaExpandida(func.id, 'sistemas') }"
              class="clicavel sistemas-celula">
            <span v-if="func.sistemas && func.sistemas.length">
              {{ func.sistemas.map(s => `${s.nome} (${s.status})`).join(', ') }}
            </span>
            <span v-else>Nenhum sistema vinculado</span>
          </td>
          <td>
            <button class="btn-editar" @click="abrirEditar(func)">✏️</button>
            <button class="btn-excluir" @click="excluirFuncionario(func.id)">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="showForm" class="modal-overlay">
      <div class="form-modal">
        <h3>{{ editando ? 'Editar Funcionário' : 'Adicionar Funcionário' }}</h3>
        <form @submit.prevent="editando ? salvarEdicaoFuncionario() : cadastrarFuncionario()">
          <div class="modal-row">
            <div class="modal-col">
              <input v-model="form.nome" placeholder="Nome" required />
              <input v-model="form.sobrenome" placeholder="Sobrenome" required />
              <input v-model="form.cargo" placeholder="Cargo" required />
            </div>
            <div class="modal-col">
              <input v-model="form.celular" placeholder="Celular" required />
              <input v-model="form.email" placeholder="E-mail" required type="email" />
            </div>
          </div>
          <hr class="modal-divider" />
          <div class="modal-row">
            <div class="modal-col">
              <!-- Grupos de E-mail com Select Múltiplo -->
              <div class="select-group">
                <label>Grupos de E-mail:</label>
                <div class="multi-select-container">
                  <div class="selected-items">
                    <span v-for="id in form.grupos_email_ids" :key="id" class="selected-chip">
                      {{ getGrupoNome(id) }}
                      <button type="button" @click="removeGrupo(id)" class="remove-chip">×</button>
                    </span>
                  </div>
                  <select v-model="novoGrupoId" @change="addGrupo" class="multi-select">
                    <option value="">+ Adicionar grupo...</option>
                    <option v-for="grupo in gruposEmailDisponiveis" :key="grupo.id" :value="grupo.id">
                      {{ grupo.nome }}
                    </option>
                  </select>
                </div>
              </div>
              <!-- Setores com Select Múltiplo -->
              <div class="select-group">
                <label>Setores:</label>
                <div class="multi-select-container">
                  <div class="selected-items">
                    <span v-for="id in form.setores_ids" :key="id" class="selected-chip">
                      {{ getSetorNome(id) }}
                      <button type="button" @click="removeSetor(id)" class="remove-chip">×</button>
                    </span>
                  </div>
                  <select v-model="novoSetorId" @change="addSetor" class="multi-select">
                    <option value="">+ Adicionar setor...</option>
                    <option v-for="setor in setoresDisponiveis" :key="setor.id" :value="setor.id">
                      {{ setor.nome }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
            <div class="modal-col">
              <!-- Sistemas com Select Múltiplo -->
              <div class="select-group">
                <label>Sistemas:</label>
                <div class="multi-select-container">
                  <div class="selected-items">
                    <span v-for="id in form.sistemas_ids" :key="id" class="selected-chip">
                      {{ getSistemaNome(id) }}
                      <button type="button" @click="removeSistema(id)" class="remove-chip">×</button>
                    </span>
                  </div>
                  <select v-model="novoSistemaId" @change="addSistema" class="multi-select">
                    <option value="">+ Adicionar sistema...</option>
                    <option v-for="sistema in sistemasDisponiveis" :key="sistema.id" :value="sistema.id">
                      {{ sistema.nome }} ({{ sistema.status }})
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn-cadastrar">Salvar</button>
            <button type="button" @click="fecharModal">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { API_BASE_URL } from '../api';

export default {
  data() {
    return {
      funcionarios: [],
      setores: [],
      sistemas: [],
      showForm: false,
      editando: false,
      funcionarioEditId: null,
      form: {
        nome: '',
        sobrenome: '',
        cargo: '',
        celular: '',
        email: '',
        grupo_email: '',
        setores_ids: [],
        sistemas_ids: [],
        grupos_email_ids: [],
      },
      gruposEmail: [],
      buscaFuncionario: '',
      celulasExpandidas: new Set(), // Para controlar células expandidas
      novoGrupoId: '',
      novoSetorId: '',
      novoSistemaId: '',
    }
  },
  computed: {
    funcionariosFiltrados() {
      if (!this.buscaFuncionario) return this.funcionarios;
      const busca = this.buscaFuncionario.toLowerCase();
      return this.funcionarios.filter(f => {
        const nome = (f.nome || '').toLowerCase();
        const sobrenome = (f.sobrenome || '').toLowerCase();
        const email = (f.email || '').toLowerCase();
        const cargo = (f.cargo || '').toLowerCase();
        const celular = (f.celular || '').toLowerCase();
        return (
          nome.includes(busca) ||
          sobrenome.includes(busca) ||
          email.includes(busca) ||
          cargo.includes(busca) ||
          celular.includes(busca)
        );
      });
    },
    gruposEmailDisponiveis() {
      return this.gruposEmail.filter(grupo => !this.form.grupos_email_ids.includes(grupo.id));
    },
    setoresDisponiveis() {
      return this.setores.filter(setor => !this.form.setores_ids.includes(setor.id));
    },
    sistemasDisponiveis() {
      return this.sistemas.filter(sistema => !this.form.sistemas_ids.includes(sistema.id));
    }
  },
  async mounted() {
    await this.carregarGruposEmail();
    await this.carregarFuncionarios();
    await this.carregarSetores();
    await this.carregarSistemas();
  },
  methods: {
    async carregarGruposEmail() {
      const res = await axios.get(`${API_BASE_URL}/grupos-email/`);
      this.gruposEmail = res.data;
    },
    async carregarFuncionarios() {
      const res = await axios.get(`${API_BASE_URL}/funcionarios/`);
      this.funcionarios = res.data;
    },
    async carregarSetores() {
      const res = await axios.get(`${API_BASE_URL}/setores/`);
      this.setores = res.data;
    },
    async carregarSistemas() {
      const res = await axios.get(`${API_BASE_URL}/sistemas/`);
      this.sistemas = res.data;
    },
    abrirEditar(func) {
      this.form = {
        nome: func.nome,
        sobrenome: func.sobrenome,
        cargo: func.cargo,
        celular: func.celular,
        email: func.email,
        grupo_email: func.grupo_email || '',
        setores_ids: func.setores ? func.setores.map(s => s.id) : [],
        sistemas_ids: func.sistemas ? func.sistemas.map(s => s.id) : [],
        grupos_email_ids: func.grupos_email ? func.grupos_email.map(g => g.id) : [],
      };
      this.funcionarioEditId = func.id;
      this.editando = true;
      this.showForm = true;
      // Buscar sistemas vinculados ao funcionário
      axios.get(`${API_BASE_URL}/funcionarios/${func.id}/sistemas`).then(res => {
        this.form.sistemas_ids = res.data.map(s => s.id);
      });
    },
    async salvarEdicaoFuncionario() {
      // Envia todos os campos, inclusive se algum array estiver vazio
      await axios.put(`${API_BASE_URL}/funcionarios/${this.funcionarioEditId}`, {
        nome: this.form.nome,
        sobrenome: this.form.sobrenome,
        cargo: this.form.cargo,
        celular: this.form.celular,
        email: this.form.email || '',
        grupos_email_ids: [...this.form.grupos_email_ids],
        setores_ids: [...this.form.setores_ids],
        sistemas_ids: [...this.form.sistemas_ids]
      });
      // Aguarda atualização dos dados antes de fechar o modal
      await this.carregarFuncionarios();
      this.fecharModal();
    },
    async excluirFuncionario(id) {
      await axios.delete(`${API_BASE_URL}/funcionarios/${id}`);
      await this.carregarFuncionarios();
    },
    fecharModal() {
      this.showForm = false;
      this.editando = false;
      this.funcionarioEditId = null;
      this.form = { nome: '', sobrenome: '', cargo: '', celular: '', email: '', grupo_email: '', setores_ids: [], sistemas_ids: [], grupos_email_ids: [] };
      this.novoGrupoId = '';
      this.novoSetorId = '';
      this.novoSistemaId = '';
    },
    async cadastrarFuncionario() {
      await axios.post(`${API_BASE_URL}/funcionarios/`, {
        nome: this.form.nome,
        sobrenome: this.form.sobrenome,
        cargo: this.form.cargo,
        celular: this.form.celular,
        email: this.form.email,
        grupos_email_ids: this.form.grupos_email_ids,
        setores_ids: this.form.setores_ids,
        sistemas_ids: this.form.sistemas_ids
      });
      await this.carregarFuncionarios();
      this.fecharModal();
    },
    async cadastrarGrupoEmail() {
      await axios.post(`${API_BASE_URL}/grupos-email/`, { nome: this.formGrupo.nome });
      this.formGrupo.nome = '';
      await this.carregarGruposEmail();
    },
    abrirEditarGrupo(grupo) {
      this.formGrupo.nome = grupo.nome;
      this.grupoEditId = grupo.id;
      this.editandoGrupo = true;
    },
    async salvarEdicaoGrupo() {
      await axios.put(`${API_BASE_URL}/grupos-email/${this.grupoEditId}`, { nome: this.formGrupo.nome });
      this.formGrupo.nome = '';
      this.editandoGrupo = false;
      this.grupoEditId = null;
      await this.carregarGruposEmail();
    },
    async excluirGrupoEmail(id) {
      await axios.delete(`${API_BASE_URL}/grupos-email/${id}`);
      await this.carregarGruposEmail();
    },
    fecharModalGrupo() {
      this.showGruposEmail = false;
      this.formGrupo.nome = '';
      this.editandoGrupo = false;
      this.grupoEditId = null;
    },
    toggleCelulaExpandida(funcionarioId, coluna) {
      const key = `${funcionarioId}-${coluna}`;
      if (this.celulasExpandidas.has(key)) {
        this.celulasExpandidas.delete(key);
      } else {
        this.celulasExpandidas.add(key);
      }
      // Força a reatividade do Set
      this.celulasExpandidas = new Set(this.celulasExpandidas);
    },
    isCelulaExpandida(funcionarioId, coluna) {
      return this.celulasExpandidas.has(`${funcionarioId}-${coluna}`);
    },
    // Métodos para Select Múltiplo - Grupos
    addGrupo() {
      if (this.novoGrupoId && !this.form.grupos_email_ids.includes(parseInt(this.novoGrupoId))) {
        this.form.grupos_email_ids.push(parseInt(this.novoGrupoId));
        this.novoGrupoId = '';
      }
    },
    removeGrupo(id) {
      this.form.grupos_email_ids = this.form.grupos_email_ids.filter(gId => gId !== id);
    },
    getGrupoNome(id) {
      const grupo = this.gruposEmail.find(g => g.id === id);
      return grupo ? grupo.nome : 'Grupo não encontrado';
    },
    // Métodos para Select Múltiplo - Setores
    addSetor() {
      if (this.novoSetorId && !this.form.setores_ids.includes(parseInt(this.novoSetorId))) {
        this.form.setores_ids.push(parseInt(this.novoSetorId));
        this.novoSetorId = '';
      }
    },
    removeSetor(id) {
      this.form.setores_ids = this.form.setores_ids.filter(sId => sId !== id);
    },
    getSetorNome(id) {
      const setor = this.setores.find(s => s.id === id);
      return setor ? setor.nome : 'Setor não encontrado';
    },
    // Métodos para Select Múltiplo - Sistemas
    addSistema() {
      if (this.novoSistemaId && !this.form.sistemas_ids.includes(parseInt(this.novoSistemaId))) {
        this.form.sistemas_ids.push(parseInt(this.novoSistemaId));
        this.novoSistemaId = '';
      }
    },
    removeSistema(id) {
      this.form.sistemas_ids = this.form.sistemas_ids.filter(sId => sId !== id);
    },
    getSistemaNome(id) {
      const sistema = this.sistemas.find(s => s.id === id);
      return sistema ? sistema.nome : 'Sistema não encontrado';
    }
  }
}
</script>

<style scoped>
.tabela-funcionarios {
  background: var(--cor-branco);
  border-radius: 12px;
  padding: 24px 20px;
  margin: 20px 0 0 -8px;
  box-shadow: 0 2px 8px rgba(20,65,121,0.08);
  overflow-x: auto;
}

/* Dica de expansão */
.dica-expansao {
  text-align: center;
  margin-bottom: 16px;
  color: var(--cor-sec1);
  font-family: var(--font-corpo);
  opacity: 0.8;
}

/* Header melhorado */
.header-funcionarios {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 20px;
  gap: 20px;
}
.busca-adicionar {
  display: flex;
  gap: 16px;
  align-items: center;
}
.input-busca {
  padding: 8px 16px;
  border-radius: 8px;
  border: 1.5px solid var(--cor-sec2);
  min-width: 220px;
  font-size: 15px;
  font-family: var(--font-corpo);
  background: #f8fafc;
  transition: border 0.2s;
}
.input-busca:focus {
  border: 2px solid var(--cor-destaque);
  outline: none;
}
.header h2 {
  color: var(--cor-primaria);
  font-family: var(--font-titulo);
}
.btn-cadastrar {
  background: var(--cor-destaque);
  color: var(--cor-primaria);
  border: none;
  border-radius: 4px;
  padding: 10px 18px;
  font-size: 15px;
  font-family: var(--font-titulo);
  cursor: pointer;
  transition: background 0.2s;
}
.btn-cadastrar:hover {
  background: var(--cor-sec3);
}
table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-bottom: 16px;
  background: #fff;
  box-shadow: 0 1px 6px rgba(20,65,121,0.06);
  border-radius: 10px;
  overflow: hidden;
}
thead th {
  position: sticky;
  top: 0;
  background: var(--cor-branco);
  color: var(--cor-primaria);
  font-family: var(--font-titulo);
  font-size: 15px;
  padding: 12px 8px;
  border-bottom: 2px solid var(--cor-destaque);
  z-index: 2;
}
tbody tr {
  transition: background 0.15s;
}
tbody tr:hover {
  background: #f6f8fa;
}
td {
  padding: 10px 8px;
  border-bottom: 1.5px solid #f3e6c2;
  font-family: var(--font-corpo);
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
}

td:nth-child(1), td:nth-child(2) { max-width: 120px; } /* Nome, Sobrenome */
td:nth-child(3) { max-width: 130px; } /* Celular */
td:nth-child(4) { max-width: 180px; } /* E-mail */
td:nth-child(5), td:nth-child(6) { max-width: 140px; } /* Grupo E-mail, Setor */
td:nth-child(7) { max-width: 120px; } /* Cargo */
td:nth-child(8) { max-width: 250px; white-space: normal; } /* Sistemas - maior espaço */
td:nth-child(9) { max-width: 100px; white-space: normal; } /* Ações */

/* Estilo especial para célula de sistemas */
.sistemas-celula {
  font-size: 13px;
  line-height: 1.3;
}

.sistemas-celula.expandida {
  font-size: 14px;
  line-height: 1.4;
  padding: 12px 8px;
}

/* Células clicáveis */
td.clicavel {
  cursor: pointer;
  transition: background-color 0.2s;
  position: relative;
}

td.clicavel:hover {
  background-color: #e3f2fd;
}

/* Células expandidas */
td.expandida {
  white-space: normal !important;
  word-break: break-word !important;
  overflow: visible !important;
  text-overflow: clip !important;
  max-width: none !important;
  background-color: #f0f7ff;
  border: 2px solid var(--cor-destaque);
  z-index: 10;
  position: relative;
}

/* Indicador visual de que a célula é clicável */
td.clicavel::after {
  content: '👆';
  position: absolute;
  top: 2px;
  right: 4px;
  font-size: 10px;
  opacity: 0;
  transition: opacity 0.2s;
}

td.clicavel:hover::after {
  opacity: 0.6;
}
tbody tr:last-child td {
  border-bottom: none;
}
.btn-editar {
  background: var(--cor-sec1);
  color: var(--cor-branco);
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  margin-right: 4px;
  cursor: pointer;
  font-size: 14px;
}
.btn-excluir {
  background: #d32f2f;
  color: var(--cor-branco);
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  cursor: pointer;
  font-size: 14px;
}
/* Modal overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(20,65,121,0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.form-modal {
  background: var(--cor-branco);
  border: 1px solid var(--cor-sec1);
  border-radius: 12px;
  padding: 32px 28px;
  max-width: 600px;
  width: 96%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 24px rgba(20,65,121,0.18);
  font-family: var(--font-corpo);
}
.form-modal h3 {
  color: var(--cor-primaria);
  font-family: var(--font-titulo);
  margin-bottom: 24px;
  text-align: center;
}
.form-modal input {
  width: 100%;
  padding: 10px;
  margin-bottom: 16px;
  border: 1px solid var(--cor-sec2);
  border-radius: 4px;
  font-size: 15px;
  font-family: var(--font-corpo);
}
.form-modal input:focus {
  outline: 2px solid var(--cor-destaque);
}
.modal-actions {
  display: flex;
  justify-content: space-between;
}
.form-modal button {
  background: var(--cor-destaque);
  color: var(--cor-primaria);
  border: none;
  border-radius: 4px;
  padding: 10px 18px;
  font-size: 15px;
  font-family: var(--font-titulo);
  cursor: pointer;
  margin-right: 8px;
  transition: background 0.2s;
}
.form-modal button:last-child {
  background: var(--cor-sec1);
  color: var(--cor-branco);
  margin-right: 0;
}
.form-modal button:hover {
  background: var(--cor-sec3);
}

/* Estilos para Select Múltiplo */
.select-group {
  margin-bottom: 20px;
}

.select-group label {
  font-weight: bold;
  margin-bottom: 8px;
  display: block;
  color: var(--cor-primaria);
  font-family: var(--font-titulo);
}

.multi-select-container {
  border: 1px solid var(--cor-sec2);
  border-radius: 6px;
  padding: 8px;
  background: #f8fafc;
  min-height: 80px;
}

.selected-items {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
  min-height: 32px;
}

.selected-chip {
  background: var(--cor-destaque);
  color: var(--cor-primaria);
  padding: 4px 8px;
  border-radius: 16px;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-corpo);
}

.remove-chip {
  background: none;
  border: none;
  color: var(--cor-primaria);
  font-size: 16px;
  cursor: pointer;
  padding: 0;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.remove-chip:hover {
  background: rgba(20,65,121,0.1);
}

.multi-select {
  width: 100%;
  padding: 6px 8px;
  border: 1px solid var(--cor-sec2);
  border-radius: 4px;
  background: white;
  font-family: var(--font-corpo);
  font-size: 14px;
  color: var(--cor-primaria);
}

.multi-select:focus {
  outline: 2px solid var(--cor-destaque);
}

.multi-select option {
  padding: 8px;
}

/* Modal responsivo melhorado */
.form-modal {
  background: var(--cor-branco);
  border: 1px solid var(--cor-sec1);
  border-radius: 8px;
  padding: 24px;
  max-width: 500px;
  width: 90%;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(20,65,121,0.2);
  font-family: var(--font-corpo);
}

.modal-row {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  margin-bottom: 18px;
}
.modal-col {
  flex: 1;
  min-width: 220px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.modal-divider {
  border: none;
  border-top: 1.5px solid var(--cor-sec2);
  margin: 18px 0;
}

@media (max-width: 768px) {
  .form-modal {
    max-width: 99%;
    padding: 16px;
  }
  .modal-row {
    flex-direction: column;
    gap: 10px;
  }
  .modal-col {
    min-width: 100%;
    gap: 8px;
  }
  
  .selected-items {
    min-height: 24px;
  }
  
  .selected-chip {
    font-size: 12px;
    padding: 3px 6px;
  }
}
</style>
