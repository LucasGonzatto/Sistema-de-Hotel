const API_URL = "http://127.0.0.1:8000";

async function carregarClientes() {

  const resposta = await fetch(
    `${API_URL}/clientes`
  );

  const clientes = await resposta.json();

  const tabela = document.getElementById(
    "client-table-body"
  );

  tabela.innerHTML = "";

  clientes.forEach(cliente => {

    tabela.innerHTML += `

      <tr>

        <td>${cliente.descricao}</td>

        <td>${cliente.check_in}</td>

        <td>${cliente.check_out}</td>

        <td>${cliente.quarto}</td>

        <td>
          <span class="badge ${cliente.status}">
            ${cliente.status}
          </span>
        </td>

        <td>
          <button
            class="delete-btn"
            onclick="deletarCliente(${cliente.id})"
          >
            Excluir
          </button>
        </td>

      </tr>
    `;
  });
}

document
  .getElementById("cliente-form")
  .addEventListener("submit", async (e) => {

    e.preventDefault();

    const checkIn =
      document.getElementById("check_in").value;

    const checkOut =
      document.getElementById("check_out").value;

    // VALIDAR DATAS
    if (checkOut <= checkIn) {

      alert(
        "Check-out deve ser após check-in"
      );

      return;
    }

    const cliente = {

      descricao:
        document.getElementById("descricao").value,

      check_in: checkIn,

      check_out: checkOut,

      quarto: parseInt(
        document.getElementById("quarto").value
      ),

      status:
        document.getElementById("status").value
    };

    const resposta = await fetch(
      `${API_URL}/clientes`,
      {

        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify(cliente)
      }
    );

    const resultado = await resposta.json();

    if (!resposta.ok) {

      alert(resultado.detail);

      return;
    }

    alert("Cliente cadastrado!");

    document
      .getElementById("cliente-form")
      .reset();

    carregarClientes();
});

async function deletarCliente(id) {

  const confirmar = confirm(
    "Deseja excluir este cliente?"
  );

  if (!confirmar) return;

  await fetch(
    `${API_URL}/clientes/${id}`,
    {
      method: "DELETE"
    }
  );

  carregarClientes();
}

carregarClientes();